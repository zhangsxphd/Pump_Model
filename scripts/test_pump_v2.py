import math
from build123d import *

def build_pump():
    # Z=0 is the mounting plate front surface.
    # Motor is in Z < 0.
    # Pump head is in Z > 0.
    
    # Motor body: dia 27.5, length 37.0 (Z from -52.5 to -15.5)
    motor = Pos(0, 0, -15.5 - 37.0 / 2) * Cylinder(radius=27.5 / 2, height=37.0)
    
    # Motor rear boss
    boss = Pos(0, 0, -52.5 - 1.0) * Cylinder(radius=7.0 / 2, height=2.0)
    
    # Motor terminals
    t1 = Pos(-6, 0, -52.5 - 2.0) * Box(1.5, 3.5, 4.0)
    t2 = Pos(6, 0, -52.5 - 2.0) * Box(1.5, 3.5, 4.0)
    
    # Collar / gearbox: dia 31.5, length 11.5 (Z from -15.5 to -4.0)
    collar = Pos(0, 0, -4.0 - 11.5 / 2) * Cylinder(radius=31.5 / 2, height=11.5)
    
    # Flange: thickness 4.0 (Z from -4.0 to 0)
    # Ear-to-ear 56.6, holes at +/- 24.25
    with BuildSketch() as sk_flange:
        Circle(radius=37.5 / 2)
        with Locations((-24.25, 0), (24.25, 0)):
            Circle(radius=4.05)
        Rectangle(48.5, 8.1)
        with Locations((-24.25, 0), (24.25, 0)):
            Circle(radius=3.2 / 2, mode=Mode.SUBTRACT)
    flange = Pos(0, 0, -2.0) * extrude(sk_flange.sketch, amount=2.0, both=True)
    
    # Pump head main body: dia 37.5, length 24.0 (Z from 0 to 24.0)
    with BuildSketch() as sk_head:
        Circle(radius=37.5 / 2)
        # Top manifold block (height 40.6 mm from bottom -18.75 to +21.85)
        with Locations((0, 14.5)):
            Rectangle(22.0, 14.7)
    head_body = Pos(0, 0, 12.0) * extrude(sk_head.sketch, amount=12.0, both=True)
    
    # Front decorative rim and window (Z from 24.0 to 25.5)
    with BuildSketch() as sk_rim:
        Circle(radius=36.0 / 2)
        Circle(radius=32.0 / 2, mode=Mode.SUBTRACT)
    rim = Pos(0, 0, 24.0 + 0.75) * extrude(sk_rim.sketch, amount=0.75, both=True)
    
    with BuildSketch() as sk_win:
        Circle(radius=31.5 / 2)
    win = Pos(0, 0, 24.0 + 0.4) * extrude(sk_win.sketch, amount=0.4, both=True)
    
    # Nozzles: 2 barbed connectors on top (+Y direction)
    # Centered at Z = 12.0, X = +/- 6.5, Y starting at 21.85
    nozzle_z = 17.0
    nozzles = []
    for nx in [-6.5, 6.5]:
        # base tube
        n_base = Pos(nx, 21.85 + 3.0, nozzle_z) * Rot(X=-90) * Cylinder(radius=4.0 / 2, height=6.0)
        # barb 1
        b1 = Pos(nx, 21.85 + 6.0 + 2.0, nozzle_z) * Rot(X=-90) * Cone(bottom_radius=5.2 / 2, top_radius=3.8 / 2, height=4.0)
        # barb 2
        b2 = Pos(nx, 21.85 + 10.0 + 2.0, nozzle_z) * Rot(X=-90) * Cone(bottom_radius=5.2 / 2, top_radius=3.8 / 2, height=4.0)
        # tip tube
        n_tip = Pos(nx, 21.85 + 14.0 + 4.0, nozzle_z) * Rot(X=-90) * Cylinder(radius=3.5 / 2, height=8.0)
        nozzles.extend([n_base, b1, b2, n_tip])
        
    parts = [motor, boss, t1, t2, collar, flange, head_body, rim, win] + nozzles
    pump = Compound(parts)
    return pump

if __name__ == "__main__":
    pump = build_pump()
    export_step(pump, "/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/scratch/kef_pump_v2.step")
    print("V2 Exported successfully!")
