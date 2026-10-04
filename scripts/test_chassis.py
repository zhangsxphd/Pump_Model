import math
from build123d import *

def build_chassis():
    # Outer dimensions
    W = 352.0
    H = 172.0
    D = 145.0
    WALL = 4.0
    
    # 1. Main outer body with rounded corners
    with BuildPart() as p:
        with BuildSketch() as sk:
            RectangleRounded(W, H, radius=14.0)
        extrude(amount=D)
        
        # Fillet back outer edges
        # back face is at Z = 0, front face is at Z = D
        back_edges = p.edges().filter_by(Axis.Z).group_by(SortBy.LENGTH)[-1]
        
        # Hollow out the inside from front (Z = D):
        # Interior depth is D - WALL = 141.0 mm (back wall is WALL = 4 mm thick)
        with BuildSketch(Plane.XY.offset(WALL)) as sk_inner:
            RectangleRounded(W - 2 * WALL, H - 2 * WALL, radius=10.0)
        extrude(amount=D - WALL, mode=Mode.SUBTRACT)
        
        # Front bezel recess for acrylic window (at Z = D - 3.2 mm to D)
        # Acrylic window size: 334 x 154 x 3.0 mm
        with BuildSketch(Plane.XY.offset(D - 3.2)) as sk_recess:
            RectangleRounded(336.0, 156.0, radius=10.0)
        extrude(amount=3.2, mode=Mode.SUBTRACT)
        
        # 4 Corner screw bosses for acrylic front cover (at Z = D - 15 to D - 3.2)
        # Positioned in the 4 corners of the recess
        boss_xs = [-158.0, 158.0]
        boss_ys = [-68.0, 68.0]
        for bx in boss_xs:
            for by in boss_ys:
                with Locations((bx, by, D - 15.0)):
                    Cylinder(radius=5.0, height=11.8)
                with Locations((bx, by, D - 15.0)):
                    Cylinder(radius=3.2 / 2, height=15.0, mode=Mode.SUBTRACT)
                    
        # 4 Bottom foot pads (at Y = -H/2 = -86.0 mm, Z at 25 and D - 25, X at +/- 150)
        for fx in [-150.0, 150.0]:
            for fz in [25.0, D - 25.0]:
                with Locations((fx, -H / 2 - 3.0, fz)):
                    with BuildSketch(Plane.XZ) as sk_foot:
                        Circle(radius=10.0)
                    extrude(amount=6.0, dir=(0, -1, 0))
                    
        # Right side ventilation slots (on X = +W/2 face, i.e. X = 176.0 mm)
        # Upper group: 4 horizontal slots
        for sy in [30.0, 42.0, 54.0, 66.0]:
            with Locations((W / 2, sy, 85.0)):
                with BuildSketch(Plane.YZ) as sk_slot:
                    SlotOverall(width=32.0, height=4.0, rotation=0)
                extrude(amount=WALL + 2.0, dir=(-1, 0, 0), mode=Mode.SUBTRACT)
                
        # Lower group: 4 vertical slots
        for sz in [70.0, 80.0, 90.0, 100.0]:
            with Locations((W / 2, -35.0, sz)):
                with BuildSketch(Plane.YZ) as sk_slot:
                    SlotOverall(width=28.0, height=4.0, rotation=90)
                extrude(amount=WALL + 2.0, dir=(-1, 0, 0), mode=Mode.SUBTRACT)
                
    return p.part

if __name__ == "__main__":
    chassis = build_chassis()
    export_step(chassis, "/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/scratch/chassis_test.step")
    print("Chassis exported successfully!")
