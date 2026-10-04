import math
from build123d import *

def build_kef_pump():
    # Coordinate system:
    # Z axis: axial along motor shaft.
    # Z = 0: front face of mounting flange (where it touches the mounting bracket)
    # Z > 0: forward into the pump head (0 to +24 mm)
    # Z < 0: backward into mounting flange (-4 to 0), collar (-15.5 to -4), motor (-52.5 to -15.5)
    # Y axis: vertical (top nozzles point in +Y direction)
    # X axis: horizontal (mounting ears extend along X)

    # 1. Mounting Flange (at Z = -4 to 0 mm)
    # Total ear-to-ear width: 56.6 mm, mounting hole pitch: 48.5 mm, hole dia: 3.2 mm
    # Flange thickness: 4.0 mm
    with BuildPart() as flange_part:
        with BuildSketch(Plane.XY) as sk_flange:
            # Central circle
            Circle(radius=37.5 / 2)
            # Ear lobes
            with Locations((-24.25, 0), (24.25, 0)):
                Circle(radius=4.05)
            # Hull or polygon connecting ears to center
            # Alternatively, draw ear trapezoid/rectangles
            with Locations((0, 0)):
                Rectangle(48.5, 8.1)
            # Mounting holes
            with Locations((-24.25, 0), (24.25, 0)):
                Circle(radius=3.2 / 2, mode=Mode.SUBTRACT)
        extrude(amount=4.0, dir=(0, 0, -1))
    flange = flange_part.part

    # 2. Collar / Gearbox section (Z = -4 to -15.5 mm, dia 31.5 mm)
    collar_len = 11.5
    with BuildPart() as collar_part:
        with BuildSketch(Plane.XY.offset(-4.0)) as sk_collar:
            Circle(radius=31.5 / 2)
        extrude(amount=collar_len, dir=(0, 0, -1))
    collar = collar_part.part

    # 3. Motor Body (Z = -15.5 to -52.5 mm, dia 27.5 mm)
    motor_len = 52.5 - 4.0 - collar_len  # 37.0 mm
    with BuildPart() as motor_part:
        with BuildSketch(Plane.XY.offset(-4.0 - collar_len)) as sk_motor:
            Circle(radius=27.5 / 2)
        extrude(amount=motor_len, dir=(0, 0, -1))
        # Rear bearing boss
        with BuildSketch(Plane.XY.offset(-52.5)) as sk_boss:
            Circle(radius=7.0 / 2)
        extrude(amount=2.0, dir=(0, 0, -1))
        # Solder terminals
        with Locations((-6, 0, -52.5 - 2.0), (6, 0, -52.5 - 2.0)):
            Box(1.5, 3.5, 4.0)
    motor = motor_part.part

    # 4. Pump Head Body (Z = 0 to 24 mm)
    # Pump head cylinder: dia 37.5 mm (R = 18.75)
    # Top ridge height from bottom: 40.6 mm (so top is at 40.6 - 18.75 = 21.85 mm)
    with BuildPart() as head_part:
        with BuildSketch(Plane.XY) as sk_head:
            Circle(radius=37.5 / 2)
            # Top manifold block where nozzles emerge
            with Locations((0, 15)):
                Rectangle(22.0, 13.7) # top extends to 15 + 6.85 = 21.85 mm
        extrude(amount=24.0, dir=(0, 0, 1))

        # Front face bevel / decorative ring (Kamoer style)
        with BuildSketch(Plane.XY.offset(24.0)) as sk_front:
            Circle(radius=35.0 / 2)
            Circle(radius=31.0 / 2, mode=Mode.SUBTRACT)
        extrude(amount=1.5, dir=(0, 0, 1))

        # Center cap
        with BuildSketch(Plane.XY.offset(24.0)) as sk_cap:
            Circle(radius=30.0 / 2)
        extrude(amount=0.8, dir=(0, 0, 1))

    pump_head = head_part.part

    # 5. Top Barbed Nozzles (2 nozzles on top, Y points up)
    # Pitch between nozzles ~13 mm -> X = -6.5 and +6.5
    # Manifold Z position ~ 12 mm
    nozzle_z = 12.0
    nozzle_base_y = 21.85
    with BuildPart() as nozzles_part:
        for nx in [-6.5, 6.5]:
            # Base cylinder
            with Locations((nx, nozzle_base_y, nozzle_z)):
                # pointing in +Y direction
                with BuildSketch(Plane.XZ) as sk_nbase:
                    Circle(radius=3.8 / 2)
                extrude(amount=6.0, dir=(0, 1, 0))
                # Barbed cones
                for barb_y in [6.0, 11.0]:
                    with BuildSketch(Plane.XZ.offset(barb_y)):
                        Circle(radius=5.2 / 2)
                    with BuildSketch(Plane.XZ.offset(barb_y + 4.0)):
                        Circle(radius=3.6 / 2)
                    loft()
                # Tip tube
                with BuildSketch(Plane.XZ.offset(19.0)):
                    Circle(radius=3.2 / 2)
                extrude(amount=5.0, dir=(0, 1, 0))
    nozzles = nozzles_part.part

    # Combine into unified pump solid
    pump = Compound([flange, collar, motor, pump_head, nozzles])
    return pump

if __name__ == "__main__":
    pump = build_kef_pump()
    export_step(pump, "/Users/zhangshuxuan/.gemini/antigravity/brain/e8596c9b-d519-4152-9e68-1b3c4d386a89/scratch/kef_pump_test.step")
    print("Exported successfully!")
