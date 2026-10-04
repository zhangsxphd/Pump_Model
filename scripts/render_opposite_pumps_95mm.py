#!/usr/bin/env python3
import tempfile
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from build123d import import_step, export_stl

step_path = '/Users/zhangshuxuan/Documents/Shapr3D_Models/8_channel_opposite_pumps_95mm.step'
out_png = '/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/opposite_pumps_95mm_3d_preview.png'

shape = import_step(step_path)

with tempfile.TemporaryDirectory() as td:
    stl_path = Path(td) / 'temp.stl'
    export_stl(shape, str(stl_path), tolerance=0.8, angular_tolerance=0.5)
    
    with open(stl_path, 'rb') as f:
        header = f.read(80)
        num_triangles = int.from_bytes(f.read(4), 'little')
        record_dtype = np.dtype([
            ('normal', '<f4', (3,)),
            ('v0', '<f4', (3,)),
            ('v1', '<f4', (3,)),
            ('v2', '<f4', (3,)),
            ('attr', '<u2')
        ])
        data = np.frombuffer(f.read(), dtype=record_dtype)
        normals = data['normal']
        tris = np.stack([data['v0'], data['v1'], data['v2']], axis=1)

fig = plt.figure(figsize=(10, 8), dpi=140)
ax = fig.add_subplot(111, projection='3d')

# Sophisticated dual-light shading
light1 = np.array([0.4, -0.6, 0.7])
light1 = light1 / np.linalg.norm(light1)
light2 = np.array([-0.5, 0.5, 0.5])
light2 = light2 / np.linalg.norm(light2)

shade = 0.30 + 0.50 * np.clip(normals @ light1, 0, 1) + 0.20 * np.clip(normals @ light2, 0, 1)
colors = np.outer(shade, np.array([0.38, 0.54, 0.78])) # Precision engineering slate blue

coll = Poly3DCollection(tris, facecolors=colors, edgecolor='none')
ax.add_collection3d(coll)

all_pts = tris.reshape(-1, 3)
min_b = all_pts.min(axis=0)
max_b = all_pts.max(axis=0)
center = (min_b + max_b) / 2
radius = (max_b - min_b).max() / 2 * 1.05

ax.set_xlim(center[0] - radius, center[0] + radius)
ax.set_ylim(center[1] - radius, center[1] + radius)
ax.set_zlim(center[2] - radius, center[2] + radius)

# Isometric perspective looking from front-left
ax.view_init(elev=28, azim=-55)
ax.axis('off')
fig.tight_layout()

plt.savefig(out_png, dpi=140, bbox_inches='tight', transparent=False, facecolor='white')
plt.close()
print("Saved 3D render preview to", out_png)
