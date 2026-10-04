import math
import os
from build123d import *

EXPORT_DIR = "/Users/zhangshuxuan/Documents/Shapr3D_Models"
os.makedirs(EXPORT_DIR, exist_ok=True)

# ==============================================================================
# KEY CONSTRAINTS: MAX ENVELOPE <= 250 x 250 mm (25 x 25 cm)
# Width = 246.0 mm (<= 250 mm)
# Height = 176.0 mm (<= 250 mm, with feet 182.0 mm)
# Depth = 126.0 mm (<= 250 mm, with pump heads 151.5 mm)
# ==============================================================================

# ==============================================================================
# 1. KEF PERISTALTIC PUMP (Single precision fused solid)
# ==============================================================================
def create_kef_pump_solid():
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
    
    # Top Barbed Nozzles: Z = 21.0, Y > 21.85
    nozzle_z = 21.0
    for nx in [-6.5, 6.5]:
        nb = Pos(nx, 24.5, nozzle_z) * Rot(X=-90) * Cylinder(radius=4.0 / 2, height=6.5)
        b1 = Pos(nx, 29.5, nozzle_z) * Rot(X=-90) * Cone(bottom_radius=5.2 / 2, top_radius=3.8 / 2, height=4.2)
        b2 = Pos(nx, 33.5, nozzle_z) * Rot(X=-90) * Cone(bottom_radius=5.2 / 2, top_radius=3.8 / 2, height=4.2)
        nt = Pos(nx, 39.5, nozzle_z) * Rot(X=-90) * Cylinder(radius=3.5 / 2, height=8.2)
        pump = pump + nb + b1 + b2 + nt
        
    return pump


# ==============================================================================
# 2. COMPACT FRONT MOUNTING PANEL (238 x 166 x 4 mm)
# ==============================================================================
def create_front_panel(pump_xs, pump_ys):
    PANEL_W = 238.0
    PANEL_H = 166.0
    PANEL_THICK = 4.0
    
    with BuildSketch(Plane.XY.offset(-PANEL_THICK)) as sk:
        RectangleRounded(PANEL_W, PANEL_H, radius=10.0)
        
        # 4 Corner screw holes to chassis bosses
        for bx in [-108.0, 108.0]:
            for by in [-72.0, 72.0]:
                with Locations((bx, by)):
                    Circle(radius=3.5 / 2, mode=Mode.SUBTRACT)
                    
        # 8 Pump Cutouts (central Φ33mm hole + 2 x M3 screw holes at 48.5mm pitch)
        for py in pump_ys:
            for px in pump_xs:
                with Locations((px, py)):
                    Circle(radius=33.0 / 2, mode=Mode.SUBTRACT)
                    with Locations((-24.25, 0), (24.25, 0)):
                        Circle(radius=3.2 / 2, mode=Mode.SUBTRACT)
                        
    panel = extrude(sk.sketch, amount=PANEL_THICK, dir=(0, 0, 1))
    return panel


# ==============================================================================
# 3. COMPACT CHASSIS ENCLOSURE (246 x 176 x 126 mm <= 250 x 250 mm)
# ==============================================================================
def create_chassis_enclosure():
    W = 246.0      # <= 250 mm (24.6 cm)
    H = 176.0      # <= 250 mm (17.6 cm)
    D = 126.0      # <= 250 mm (12.6 cm)
    WALL = 4.0
    PANEL_THICK = 4.0
    
    # Outer box: Z from -D to 0
    with BuildSketch(Plane.XY.offset(-D)) as sk_outer:
        RectangleRounded(W, H, radius=14.0)
    outer = extrude(sk_outer.sketch, amount=D, dir=(0, 0, 1))
    
    # Inner void: Z from -D + WALL to -PANEL_THICK
    with BuildSketch(Plane.XY.offset(-D + WALL)) as sk_inner:
        RectangleRounded(W - 2 * WALL, H - 2 * WALL, radius=10.0)
    inner = extrude(sk_inner.sketch, amount=D - WALL - PANEL_THICK, dir=(0, 0, 1))
    
    # Front bezel recess for front panel
    with BuildSketch(Plane.XY.offset(-PANEL_THICK)) as sk_rec:
        RectangleRounded(238.0, 166.0, radius=10.0)
    recess = extrude(sk_rec.sketch, amount=PANEL_THICK, dir=(0, 0, 1))
    
    body = outer - inner - recess
    
    # 4 Corner bosses for front panel screws (Z from -16.0 to -PANEL_THICK = -4.0, height 12.0)
    for bx in [-108.0, 108.0]:
        for by in [-72.0, 72.0]:
            b = Pos(bx, by, -10.0) * Cylinder(radius=5.5, height=12.0)
            bh = Pos(bx, by, -9.0) * Cylinder(radius=3.2 / 2, height=14.0)
            body = (body + b) - bh
            
    # 4 Bottom Foot Pads (radius 10mm, height 6mm, centered at X = +/- 100, Z at -D+25, -25)
    for fx in [-100.0, 100.0]:
        for fz in [-D + 25.0, -25.0]:
            ft = Pos(fx, -H/2 - 3.0 + 0.25, fz) * Rot(X=90) * Cylinder(radius=10.0, height=6.5)
            body = body + ft
            
    # Side Ventilation Slots (X = W/2 = 123 mm and X = -W/2 = -123 mm)
    # Right side slots
    for sz in [-55.0, -35.0]:
        slot_r_up = Pos(W / 2, 35.0, sz) * Box(WALL * 2 + 2, 32.0, 5.0)
        slot_r_dn = Pos(W / 2, -35.0, sz) * Box(WALL * 2 + 2, 32.0, 5.0)
        body = body - slot_r_up - slot_r_dn
    # Left side slots
    for sz in [-55.0, -35.0]:
        slot_l_up = Pos(-W / 2, 35.0, sz) * Box(WALL * 2 + 2, 32.0, 5.0)
        slot_l_dn = Pos(-W / 2, -35.0, sz) * Box(WALL * 2 + 2, 32.0, 5.0)
        body = body - slot_l_up - slot_l_dn
        
    # Rear DC 12V power inlet hole at Z = -D (center X = 0, Y = -60)
    dc_hole = Pos(0.0, -60.0, -D) * Cylinder(radius=6.0, height=WALL * 2 + 2)
    body = body - dc_hole
    
    # Middle partition / support plate behind motors (at Z = -60.0 mm)
    # Separates motor front bay from rear electronics bay
    # Motors extend to Z = -52.5 mm, so Z = -60 mm gives 7.5 mm clearance
    partition = Pos(0.0, 0, -60.0) * Box(W - 2 * WALL, H - 2 * WALL, WALL)
    # Cable cutouts through partition
    wire_cutout1 = Pos(-50.0, -20.0, -60.0) * Box(40.0, 30.0, WALL + 2)
    wire_cutout2 = Pos(50.0, -20.0, -60.0) * Box(40.0, 30.0, WALL + 2)
    body = body + (partition - wire_cutout1 - wire_cutout2)
    
    return body


# ==============================================================================
# 4. REAR ELECTRONIC MODULES (8-Channel Relay, PSU, MCU in Rear Bay)
# ==============================================================================
def create_electronic_modules():
    """
    Electronics are housed in the rear bay (Z from -62 to -122 mm, width 238 mm).
    8-channel relay board is mounted across the rear partition (X = 0, Z = -85 mm).
    12V Power supply module sits in lower rear (X = 55, Y = -50, Z = -100 mm).
    MCU / WiFi sits at (X = -60, Y = -50, Z = -100 mm).
    """
    # 8-Channel Relay Board (138 x 56 x 1.6 mm) mounted horizontally across rear partition
    relay_board = Pos(0.0, 15.0, -85.0) * Box(136.0, 52.0, 1.6)
    for rx in range(8):
        pos_x = -49.0 + rx * 14.0
        relay_cube = Pos(pos_x, 15.0, -76.7) * Box(12.0, 16.0, 15.0)
        relay_board = relay_board + relay_cube
    tb_left = Pos(-62.0, 15.0, -79.2) * Box(8.0, 48.0, 10.0)
    tb_right = Pos(62.0, 15.0, -79.2) * Box(8.0, 48.0, 10.0)
    relay_board = relay_board + tb_left + tb_right
    
    # 12V Power Supply Module (Lower right)
    psu_box = Pos(50.0, -50.0, -95.0) * Box(65.0, 38.0, 34.0)
    
    # MCU / WiFi Module (Lower left)
    mcu_pcb = Pos(-50.0, -50.0, -95.0) * Box(45.0, 30.0, 12.0)
    
    return [relay_board, psu_box, mcu_pcb]


# ==============================================================================
# 5. MASTER BUILD & EXPORT
# ==============================================================================
def build_all():
    print("Building KEF Peristaltic Pump...")
    single_pump = create_kef_pump_solid()
    pump_step_path = os.path.join(EXPORT_DIR, "kef_peristaltic_pump.step")
    export_step(single_pump, pump_step_path)
    print(f"Exported: {pump_step_path}")
    
    # 4 pumps horizontally with pitch 58.0 mm (symmetric: -87, -29, +29, +87)
    pump_xs = [-87.0, -29.0, 29.0, 87.0]
    # 2 rows vertically with pitch 68.0 mm (symmetric: -34, +34)
    pump_ys = [-34.0, 34.0]
    
    print("Building 25cm Compact Front Mounting Panel...")
    front_panel = create_front_panel(pump_xs, pump_ys)
    panel_step_path = os.path.join(EXPORT_DIR, "front_mounting_panel.step")
    export_step(front_panel, panel_step_path)
    print(f"Exported: {panel_step_path}")
    
    print("Building 25cm Compact Chassis Enclosure...")
    chassis = create_chassis_enclosure()
    chassis_step_path = os.path.join(EXPORT_DIR, "chassis_enclosure.step")
    export_step(chassis, chassis_step_path)
    print(f"Exported: {chassis_step_path}")
    
    print("Building Electronic Modules...")
    elec_list = create_electronic_modules()
    elec_compound = Compound(elec_list)
    elec_step_path = os.path.join(EXPORT_DIR, "electronic_modules.step")
    export_step(elec_compound, elec_step_path)
    print(f"Exported: {elec_step_path}")
    
    print("Assembling 25cm Compact 8-Channel Pump Station...")
    pumps_assembly = []
    for py in pump_ys:
        for px in pump_xs:
            placed_pump = Pos(px, py, 0.0) * single_pump
            pumps_assembly.append(placed_pump)
            
    full_assembly_parts = [
        chassis,
        front_panel,
    ] + elec_list + pumps_assembly
    
    full_assembly = Compound(full_assembly_parts)
    assembly_step_path = os.path.join(EXPORT_DIR, "8_channel_pump_station_assembly.step")
    export_step(full_assembly, assembly_step_path)
    print(f"Exported: {assembly_step_path}")
    
    return {
        "pump": pump_step_path,
        "panel": panel_step_path,
        "chassis": chassis_step_path,
        "electronics": elec_step_path,
        "assembly": assembly_step_path,
    }

if __name__ == "__main__":
    paths = build_all()
    print("Compact <= 25cm models successfully built and exported!")
