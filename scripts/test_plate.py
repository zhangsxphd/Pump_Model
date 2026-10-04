import math
from build123d import *

def build_mounting_plate():
    # Width 258 mm, Height 156 mm, Thickness 4.0 mm
    # 8 pump positions: 2 rows of 4
    pump_xs = [-128.0, -66.0, -4.0, 58.0]
    pump_ys = [-32.0, 38.0]
    
    with BuildPart() as p:
        # Base plate
        with BuildSketch() as sk:
            RectangleRounded(256.0, 154.0, radius=6.0)
            
            # 8 pump cutouts
            for py in pump_ys:
                for px in pump_xs:
                    with Locations((px, py)):
                        # Center motor hole (dia 33.0 mm)
                        Circle(radius=33.0 / 2, mode=Mode.SUBTRACT)
                        # Two M3 mounting screw holes (dia 3.2 mm, pitch 48.5 mm)
                        with Locations((-24.25, 0), (24.25, 0)):
                            Circle(radius=3.2 / 2, mode=Mode.SUBTRACT)
                            
            # Tube routing slots below bottom row
            for px in pump_xs:
                with Locations((px, -65.0)):
                    SlotOverall(width=22.0, height=8.0, rotation=0, mode=Mode.SUBTRACT)
                    
            # 4 chassis mounting screw holes at corners
            with Locations((-118.0, -68.0), (-118.0, 68.0), (118.0, -68.0), (118.0, 68.0)):
                Circle(radius=3.5 / 2, mode=Mode.SUBTRACT)
                
        extrude(amount=4.0)
        
    return p.part

if __name__ == "__main__":
    plate = build_mounting_plate()
    export_step(plate, "/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/scratch/pump_mounting_plate_test.step")
    print("Mounting plate exported successfully!")
