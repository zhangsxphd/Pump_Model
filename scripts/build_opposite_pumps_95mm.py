#!/usr/bin/env python3
"""
8-Channel Peristaltic Pump Station - Opposite Mounting Design (9.5cm Width)
- Board Width: 95.0 mm (9.5 cm)
- Board Height: 240.0 mm (24.0 cm <= 25.0 cm)
- Left 4 pumps: Nozzles face LEFT (<- Front outlet direction)
- Right 4 pumps: Nozzles face RIGHT (-> Rear outlet direction)
- Middle area: Central partition / wiring channel (11.5 mm clear gap)
- All dimensions <= 250 x 250 mm (25 x 25 cm)
"""

import math
import os
from build123d import *

EXPORT_DIR = "/Users/zhangshuxuan/Documents/Shapr3D_Models"
os.makedirs(EXPORT_DIR, exist_ok=True)

# ---------------------------------------------------------
# 1. KEF Parametric Peristaltic Pump Model
# ---------------------------------------------------------
def create_kef_pump_solid():
    """
    Creates a single KEF peristaltic pump.
    In local coords:
    - Flange at Z=0..4.0mm, ears along X at X=+-24.25mm
    - Motor collar & motor along -Z
    - Pump head body at Z=4.0..28.0mm
    - Nozzles point along +Y (default)
    """
    # Flange: Z from 0 to 4.0 mm
    with BuildSketch() as sk_flange:
        Circle(radius=37.5 / 2)
        with Locations((-24.25, 0), (24.25, 0)):
            Circle(radius=4.05)
        Rectangle(48.5, 8.1)
        with Locations((-24.25, 0), (24.25, 0)):
            Circle(radius=3.2 / 2, mode=Mode.SUBTRACT)
    flange = Pos(0, 0, 2.0) * extrude(sk_flange.sketch, amount=2.0, both=True)
    
    # Collar & Motor (Z < 0)
    collar = Pos(0, 0, -5.7) * Cylinder(radius=31.5 / 2, height=11.6)
    motor = Pos(0, 0, -32.0) * Cylinder(radius=27.5 / 2, height=41.2)
    boss = Pos(0, 0, -53.5) * Cylinder(radius=7.0 / 2, height=2.2)
    t1 = Pos(-6.0, 0, -54.5) * Box(1.5, 3.5, 4.2)
    t2 = Pos(6.0, 0, -54.5) * Box(1.5, 3.5, 4.2)
    
    # Pump Head Body: Z from 3.9 to 28.0 mm
    with BuildSketch() as sk_head:
        Circle(radius=37.5 / 2)
        with Locations((0, 14.5)):
            Rectangle(22.0, 14.7)
    head_body = Pos(0, 0, 16.0) * extrude(sk_head.sketch, amount=12.1, both=True)
    
    # Front rim & window: Z from 27.9 to 29.5 mm
    rim = Pos(0, 0, 28.7) * extrude(Circle(radius=36.0 / 2) - Circle(radius=32.0 / 2), amount=0.8, both=True)
    win = Pos(0, 0, 28.4) * extrude(Circle(radius=31.5 / 2), amount=0.5, both=True)
    
    pump = flange + collar + motor + boss + t1 + t2 + head_body + rim + win
    
    # Top Barbed Nozzles: Z = 21.0, Y > 21.85 (pointing along +Y)
    nozzle_z = 21.0
    for nx in [-6.5, 6.5]:
        nb = Pos(nx, 24.5, nozzle_z) * Rot(X=-90) * Cylinder(radius=4.0 / 2, height=6.5)
        b1 = Pos(nx, 29.5, nozzle_z) * Rot(X=-90) * Cone(bottom_radius=5.2 / 2, top_radius=3.8 / 2, height=4.2)
        b2 = Pos(nx, 33.5, nozzle_z) * Rot(X=-90) * Cone(bottom_radius=5.2 / 2, top_radius=3.8 / 2, height=4.2)
        nt = Pos(nx, 39.5, nozzle_z) * Rot(X=-90) * Cylinder(radius=3.5 / 2, height=8.2)
        pump = pump + nb + b1 + b2 + nt
        
    return pump


# ---------------------------------------------------------
# 2. Dimensions & Coordinates
# ---------------------------------------------------------
PANEL_W = 95.0    # 9.5 cm width
PANEL_H = 240.0   # 24.0 cm height (<= 25 cm)
PANEL_THICK = 4.0 # 4 mm plate

CHASSIS_W = 95.0
CHASSIS_H = 240.0
CHASSIS_D = 72.0
CHASSIS_WALL = 3.5

PUMP_YS = [-87.0, -29.0, 29.0, 87.0] # Pitch 58.0 mm
X_LEFT = -24.5   # Left column
X_RIGHT = 24.5   # Right column

CORNER_X = 38.0
CORNER_Y = 110.0


# ---------------------------------------------------------
# 3. Create 9.5cm Front Mounting Panel
# ---------------------------------------------------------
def create_front_panel():
    with BuildSketch(Plane.XY.offset(-PANEL_THICK)) as sk:
        RectangleRounded(PANEL_W, PANEL_H, radius=6.0)
        
        # 4 Corner mounting holes M3
        for cx in [-CORNER_X, CORNER_X]:
            for cy in [-CORNER_Y, CORNER_Y]:
                with Locations((cx, cy)):
                    Circle(radius=3.5 / 2, mode=Mode.SUBTRACT)

        # Left Column Cutouts (Rotated 90 deg: ears are along Y at py +- 24.25)
        for py in PUMP_YS:
            with Locations((X_LEFT, py)):
                Circle(radius=33.0 / 2, mode=Mode.SUBTRACT)
                with Locations((0, -24.25), (0, 24.25)):
                    Circle(radius=3.2 / 2, mode=Mode.SUBTRACT)

        # Right Column Cutouts (Rotated -90 deg: ears are along Y at py +- 24.25)
        for py in PUMP_YS:
            with Locations((X_RIGHT, py)):
                Circle(radius=33.0 / 2, mode=Mode.SUBTRACT)
                with Locations((0, -24.25), (0, 24.25)):
                    Circle(radius=3.2 / 2, mode=Mode.SUBTRACT)

        # Central divider groove indicator (Width 2mm, height 200mm)
        # with Locations((0, 0)):
        #     Rectangle(2.0, 200.0, mode=Mode.SUBTRACT)

    panel = extrude(sk.sketch, amount=PANEL_THICK, dir=(0, 0, 1))
    return panel


# ---------------------------------------------------------
# 4. Create Compact Chassis Enclosure (95 x 240 x 72 mm)
# ---------------------------------------------------------
def create_chassis_enclosure():
    # Outer box: Z from -CHASSIS_D to -PANEL_THICK
    box_height = CHASSIS_D - PANEL_THICK
    with BuildSketch(Plane.XY.offset(-CHASSIS_D)) as sk_outer:
        RectangleRounded(CHASSIS_W, CHASSIS_H, radius=6.0)
    outer = extrude(sk_outer.sketch, amount=box_height, dir=(0, 0, 1))

    # Inner void: Z from -CHASSIS_D + CHASSIS_WALL to -PANEL_THICK
    inner_h = box_height - CHASSIS_WALL
    with BuildSketch(Plane.XY.offset(-CHASSIS_D + CHASSIS_WALL)) as sk_inner:
        RectangleRounded(CHASSIS_W - 2 * CHASSIS_WALL, CHASSIS_H - 2 * CHASSIS_WALL, radius=4.0)
    inner = extrude(sk_inner.sketch, amount=inner_h + 0.1, dir=(0, 0, 1))

    body = outer - inner

    # 4 Corner Standoff Bosses for M3 screws (Z from -16.0 to -PANEL_THICK = -4.0)
    for cx in [-CORNER_X, CORNER_X]:
        for cy in [-CORNER_Y, CORNER_Y]:
            b = Pos(cx, cy, -10.0) * Cylinder(radius=5.0, height=12.0)
            bh = Pos(cx, cy, -9.0) * Cylinder(radius=3.0 / 2, height=14.0)
            body = (body + b) - bh

    # Side Ventilation Slots (Left and Right side walls)
    # Long sides at Y = +/- 60, +/- 20
    for vy in [-60.0, -20.0, 20.0, 60.0]:
        slot_r = Pos(CHASSIS_W / 2, vy, -CHASSIS_D / 2) * Box(CHASSIS_WALL * 2 + 2, 20.0, 4.0)
        slot_l = Pos(-CHASSIS_W / 2, vy, -CHASSIS_D / 2) * Box(CHASSIS_WALL * 2 + 2, 20.0, 4.0)
        body = body - slot_r - slot_l

    # Bottom support feet (on back surface Z = -CHASSIS_D)
    for fx in [-CORNER_X, CORNER_X]:
        for fy in [-CORNER_Y, CORNER_Y]:
            ft = Pos(fx, fy, -CHASSIS_D - 2.5) * Cylinder(radius=7.0, height=5.0)
            body = body + ft

    return body


# ---------------------------------------------------------
# 5. Main Execution & Assembly
# ---------------------------------------------------------
def main():
    print("Creating precision KEF pump solid...")
    kef_base = create_kef_pump_solid()

    print("Building left and right pump groups (Opposite directions)...")
    # Left column: Rotate Z=+90 deg -> Nozzles point to -X (Left / Front outlet <-)
    left_pumps = [Pos(X_LEFT, py, 0.0) * Rot(Z=90) * kef_base for py in PUMP_YS]

    # Right column: Rotate Z=-90 deg -> Nozzles point to +X (Right / Rear outlet ->)
    right_pumps = [Pos(X_RIGHT, py, 0.0) * Rot(Z=-90) * kef_base for py in PUMP_YS]

    print("Creating 9.5cm mounting panel...")
    panel = create_front_panel()

    print("Creating chassis enclosure...")
    chassis = create_chassis_enclosure()

    all_solids = [chassis, panel] + left_pumps + right_pumps
    assembly = Compound(all_solids)

    bbox = assembly.bounding_box()
    print("=" * 60)
    print("ASSEMBLY ENVELOPE DIMENSIONS:")
    print(f"X (Width):  {bbox.min.X:.2f} to {bbox.max.X:.2f} (Total = {bbox.size.X:.2f} mm / {bbox.size.X/10:.2f} cm)")
    print(f"Y (Height): {bbox.min.Y:.2f} to {bbox.max.Y:.2f} (Total = {bbox.size.Y:.2f} mm / {bbox.size.Y/10:.2f} cm)")
    print(f"Z (Depth):  {bbox.min.Z:.2f} to {bbox.max.Z:.2f} (Total = {bbox.size.Z:.2f} mm / {bbox.size.Z/10:.2f} cm)")
    print("=" * 60)

    # Verification against 25x25cm
    w_ok = bbox.size.X <= 250.0
    h_ok = bbox.size.Y <= 250.0
    d_ok = bbox.size.Z <= 250.0
    print(f"Constraints Check: W<25cm: {w_ok}, H<25cm: {h_ok}, D<25cm: {d_ok}")

    print("Exporting STEP files...")
    export_step(panel, os.path.join(EXPORT_DIR, "front_mounting_panel_95mm.step"))
    export_step(chassis, os.path.join(EXPORT_DIR, "chassis_enclosure_95mm.step"))
    export_step(assembly, os.path.join(EXPORT_DIR, "8_channel_pump_station_assembly.step"))
    export_step(assembly, os.path.join(EXPORT_DIR, "8_channel_opposite_pumps_95mm.step"))

    print("All exports completed successfully!")

if __name__ == "__main__":
    main()
