import math
from build123d import *

def test_chassis_solid():
    W = 352.0
    H = 176.0
    D = 146.0
    WALL = 4.0
    
    # Outer box: Z from -D to 0
    # In Plane.XY, extrude in +Z from -D
    with BuildSketch(Plane.XY.offset(-D)) as sk_outer:
        RectangleRounded(W, H, radius=14.0)
    outer = extrude(sk_outer.sketch, amount=D)
    
    # Inner void: Z from -D + WALL to 0
    with BuildSketch(Plane.XY.offset(-D + WALL)) as sk_inner:
        RectangleRounded(W - 2 * WALL, H - 2 * WALL, radius=10.0)
    inner = extrude(sk_inner.sketch, amount=D - WALL)
    
    body = outer - inner
    
    # Front acrylic recess: Z from -3.2 to 0
    with BuildSketch(Plane.XY.offset(-3.2)) as sk_rec:
        RectangleRounded(338.0, 162.0, radius=10.0)
    recess = extrude(sk_rec.sketch, amount=3.2)
    body = body - recess
    
    # 4 Corner bosses: cylinders at Z from -16 to -3.2 (height 12.8)
    boss_solids = []
    boss_holes = []
    for bx in [-158.0, 158.0]:
        for by in [-70.0, 70.0]:
            # Cylinder center at Z = -16 + 6.4 = -9.6
            b = Pos(bx, by, -9.6) * Cylinder(radius=5.5, height=12.8)
            bh = Pos(bx, by, -8.0) * Cylinder(radius=3.2 / 2, height=16.0)
            boss_solids.append(b)
            boss_holes.append(bh)
            
    for b in boss_solids:
        body = body + b
    for bh in boss_holes:
        body = body - bh
        
    # 4 Bottom Foot Pads: at Y = -H/2 - 3.0 (cylinder along Y, radius 10, height 6)
    # Z at -D + 25 = -121.0 and -25.0, X at -148 and +148
    feet = []
    for fx in [-148.0, 148.0]:
        for fz in [-121.0, -25.0]:
            # Cylinder along Y: height 6, center at Y = -H/2 - 3 = -91.0
            ft = Pos(fx, -H/2 - 3.0, fz) * Rot(X=90) * Cylinder(radius=10.0, height=6.0)
            feet.append(ft)
    for ft in feet:
        body = body + ft
        
    # Right side vents (X = W/2 = 176):
    # Upper slots along Z (horizontal): width along Z = 34, height along Y = 4, thickness along X = 10
    # Center X = 176, Y in [28, 40, 52, 64], Z = -70
    for sy in [28.0, 40.0, 52.0, 64.0]:
        slot = Pos(176.0, sy, -70.0) * Box(WALL * 2 + 2, 4.0, 34.0)
        body = body - slot
        
    # Lower slots along Y (vertical): width along Z = 4, height along Y = 30, thickness along X = 10
    # Center X = 176, Y = -35, Z in [-105, -90, -75, -60]
    for sz in [-105.0, -90.0, -75.0, -60.0]:
        slot = Pos(176.0, -35.0, sz) * Box(WALL * 2 + 2, 30.0, 4.0)
        body = body - slot
        
    # Rear DC power inlet hole at Z = -D (dia 12mm)
    dc_hole = Pos(135.0, -55.0, -D) * Cylinder(radius=6.0, height=WALL * 2 + 2)
    body = body - dc_hole
    
    # Internal middle partition wall at X = 102.0
    # Z from -D + WALL (-142) to -35.0 (length 107.0, center at -88.5)
    # Y from -H/2 + WALL (-84) to H/2 - WALL (+84) (height 168.0, center 0)
    # Thickness = WALL (4.0)
    partition = Pos(102.0, 0, -88.5) * Box(WALL, H - 2 * WALL, 107.0)
    # Wiring hole through partition
    wire_cutout = Pos(102.0, -20.0, -70.0) * Box(WALL + 2, 40.0, 30.0)
    body = body + (partition - wire_cutout)
    
    # Bottom front tubing exit slots (floor at Y = -H/2 + WALL = -84.0)
    # Slots through bottom wall (thickness in Y = WALL + 2, center Y = -86.0)
    # X in pump centers, Z = -18.0
    for px in [-128.0, -64.0, 0.0, 64.0]:
        tube_slot = Pos(px, -H/2 + WALL/2, -18.0) * Box(20.0, WALL + 2, 8.0)
        body = body - tube_slot
        
    return body

if __name__ == "__main__":
    chassis = test_chassis_solid()
    print("Solid count:", len(chassis.solids()))
    print("Bounding box:", chassis.bounding_box())
    export_step(chassis, "/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/scratch/chassis_algebra_test.step")
    print("Exported algebra chassis!")
