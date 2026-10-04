import math
import os
from build123d import *

EXPORT_DIR = "/Users/zhangshuxuan/Documents/Shapr3D_Models"
os.makedirs(EXPORT_DIR, exist_ok=True)

# ==============================================================================
# 1. KEF PERISTALTIC PUMP (Single precision fused solid)
# ==============================================================================
def create_kef_pump_solid():
    """
    Creates an accurate, single-solid B-rep model of the Kamoer KEF peristaltic pump.
    Origin: center of the pump mounting flange BACK face (Z = 0).
    Z+ is forward (flange thickness 4mm, then pump head 24mm).
    Z- is backward (collar 11.5mm, motor 37mm).
    Y+ is up (nozzles point along +Y).
    X is horizontal (mounting ears extend along +/- X).
    """
    # 1. Flange: Z from 0 to 4.0 mm
    with BuildSketch() as sk_flange:
        Circle(radius=37.5 / 2)
        with Locations((-24.25, 0), (24.25, 0)):
            Circle(radius=4.05)
        Rectangle(48.5, 8.1)
        with Locations((-24.25, 0), (24.25, 0)):
            Circle(radius=3.2 / 2, mode=Mode.SUBTRACT)
    flange = Pos(0, 0, 2.0) * extrude(sk_flange.sketch, amount=2.0, both=True)
    
    # 2. Collar & Motor (Z < 0, backward into chassis)
    # Collar: Z from -11.5 to 0.1 mm (overlap)
    collar = Pos(0, 0, -5.7) * Cylinder(radius=31.5 / 2, height=11.6)
    # Motor: Z from -52.5 to -11.4 mm
    motor = Pos(0, 0, -32.0) * Cylinder(radius=27.5 / 2, height=41.2)
    boss = Pos(0, 0, -53.5) * Cylinder(radius=7.0 / 2, height=2.2)
    t1 = Pos(-6.0, 0, -54.5) * Box(1.5, 3.5, 4.2)
    t2 = Pos(6.0, 0, -54.5) * Box(1.5, 3.5, 4.2)
    
    # 3. Pump Head Body: Z from 3.9 to 28.0 mm (24mm head + 4mm flange)
    with BuildSketch() as sk_head:
        Circle(radius=37.5 / 2)
        with Locations((0, 14.5)):
            Rectangle(22.0, 14.7)  # Top ridge up to Y = 21.85
    head_body = Pos(0, 0, 16.0) * extrude(sk_head.sketch, amount=12.1, both=True)
    
    # Front bezel ring & window: Z from 27.9 to 29.5 mm
    rim = Pos(0, 0, 28.7) * extrude(Circle(radius=36.0 / 2) - Circle(radius=32.0 / 2), amount=0.8, both=True)
    win = Pos(0, 0, 28.4) * extrude(Circle(radius=31.5 / 2), amount=0.5, both=True)
    
    pump = flange + collar + motor + boss + t1 + t2 + head_body + rim + win
    
    # 4. Top Barbed Nozzles: Z = 21.0 (near front of head), Y > 21.85
    nozzle_z = 21.0
    for nx in [-6.5, 6.5]:
        nb = Pos(nx, 24.5, nozzle_z) * Rot(X=-90) * Cylinder(radius=4.0 / 2, height=6.5)
        b1 = Pos(nx, 29.5, nozzle_z) * Rot(X=-90) * Cone(bottom_radius=5.2 / 2, top_radius=3.8 / 2, height=4.2)
        b2 = Pos(nx, 33.5, nozzle_z) * Rot(X=-90) * Cone(bottom_radius=5.2 / 2, top_radius=3.8 / 2, height=4.2)
        nt = Pos(nx, 39.5, nozzle_z) * Rot(X=-90) * Cylinder(radius=3.5 / 2, height=8.2)
        pump = pump + nb + b1 + b2 + nt
        
    return pump


# ==============================================================================
# 2. SOLID FRONT MOUNTING PANEL (前面板 - 8泵外置安装)
# ==============================================================================
def create_front_panel(pump_xs, pump_ys):
    """
    Creates the solid front faceplate on which the 8 pumps are externally mounted.
    Dimensions: 338.0 x 162.0 x 4.0 mm.
    Front face is at Z = 0 (where pump flange back rests).
    Back face is at Z = -4.0 mm.
    """
    PANEL_W = 338.0
    PANEL_H = 162.0
    PANEL_THICK = 4.0
    
    with BuildSketch(Plane.XY.offset(-PANEL_THICK)) as sk:
        RectangleRounded(PANEL_W, PANEL_H, radius=10.0)
        
        # 4 Corner screw holes to fasten panel to chassis
        for bx in [-158.0, 158.0]:
            for by in [-70.0, 70.0]:
                with Locations((bx, by)):
                    Circle(radius=3.5 / 2, mode=Mode.SUBTRACT)
                    
        # 8 Pump Cutouts (central Φ33mm hole + 2 x M3 screw holes at 48.5mm pitch)
        for py in pump_ys:
            for px in pump_xs:
                with Locations((px, py)):
                    # Motor clearance hole dia 33.0 mm
                    Circle(radius=33.0 / 2, mode=Mode.SUBTRACT)
                    # M3 mounting holes
                    with Locations((-24.25, 0), (24.25, 0)):
                        Circle(radius=3.2 / 2, mode=Mode.SUBTRACT)
                        
    panel = extrude(sk.sketch, amount=PANEL_THICK, dir=(0, 0, 1))
    return panel


# ==============================================================================
# 3. CHASSIS ENCLOSURE (外壳箱体 - 适用于外置泵方案)
# ==============================================================================
def create_chassis_enclosure():
    """
    Creates the 3D-printable unibody chassis.
    External dimensions: Width 352 mm, Height 176 mm, Depth 120 mm.
    Front outer bezel is at Z = 0 (flush with front panel outer surface).
    """
    W = 352.0
    H = 176.0
    D = 120.0
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
    
    # Front bezel recess for front panel: Z from -PANEL_THICK to 0
    with BuildSketch(Plane.XY.offset(-PANEL_THICK)) as sk_rec:
        RectangleRounded(338.0, 162.0, radius=10.0)
    recess = extrude(sk_rec.sketch, amount=PANEL_THICK, dir=(0, 0, 1))
    
    body = outer - inner - recess
    
    # 4 Corner bosses for front panel screws (Z from -16.0 to -PANEL_THICK)
    bosses = []
    boss_holes = []
    for bx in [-158.0, 158.0]:
        for by in [-70.0, 70.0]:
            b = Pos(bx, by, -10.0) * Cylinder(radius=5.5, height=12.0)
            bh = Pos(bx, by, -9.0) * Cylinder(radius=3.2 / 2, height=14.0)
            bosses.append(b)
            boss_holes.append(bh)
            
    for b in bosses:
        body = body + b
    for bh in boss_holes:
        body = body - bh
        
    # 4 Bottom Foot Pads (with overlap)
    for fx in [-148.0, 148.0]:
        for fz in [-D + 25.0, -25.0]:
            ft = Pos(fx, -H/2 - 3.0 + 0.25, fz) * Rot(X=90) * Cylinder(radius=10.0, height=6.5)
            body = body + ft
            
    # Right Side Ventilation Slots (X = W/2 = 176 mm)
    # Looking at the new image side view: 4 vertical slots (2 upper, 2 lower)
    # Upper vertical slots
    for sz in [-45.0, -28.0]:
        slot_up = Pos(176.0, 35.0, sz) * Box(WALL * 2 + 2, 32.0, 5.0)
        body = body - slot_up
    # Lower vertical slots
    for sz in [-45.0, -28.0]:
        slot_dn = Pos(176.0, -35.0, sz) * Box(WALL * 2 + 2, 32.0, 5.0)
        body = body - slot_dn
        
    # Rear DC power inlet hole at Z = -D
    dc_hole = Pos(136.0, -55.0, -D) * Cylinder(radius=6.0, height=WALL * 2 + 2)
    body = body - dc_hole
    
    # Internal middle partition wall at X = 100.0 mm
    # Separates motor bay from electronics bay (Z from -D + WALL to -PANEL_THICK)
    partition_len = D - WALL - PANEL_THICK  # 112 mm
    partition = Pos(100.0, 0, -D + WALL + partition_len / 2) * Box(WALL, H - 2 * WALL, partition_len)
    wire_cutout = Pos(100.0, -15.0, -70.0) * Box(WALL + 2, 45.0, 35.0)
    body = body + (partition - wire_cutout)
    
    return body


# ==============================================================================
# 4. ELECTRONIC MODULES (8-Channel Relay, PSU, MCU)
# ==============================================================================
def create_electronic_modules():
    """
    Creates clean fused representative solids for the electronics bay:
    - 8-Channel Relay Board (vertical mounted)
    - 12V Power Supply Module
    - MCU / Control Board
    """
    # 8-Channel Relay Board (Vertical at X = 136.0, Z = -75.0)
    relay_board = Pos(136.0, 8.0, -75.0) * Box(50.0, 136.0, 1.6)
    for ry in range(8):
        pos_y = -48.0 + ry * 15.0
        relay_cube = Pos(128.0, pos_y, -66.7) * Box(15.0, 12.0, 15.0)
        relay_board = relay_board + relay_cube
    tb_top = Pos(136.0, 68.0, -69.2) * Box(46.0, 10.0, 10.0)
    tb_bot = Pos(136.0, -52.0, -69.2) * Box(46.0, 10.0, 10.0)
    relay_board = relay_board + tb_top + tb_bot
    
    # MCU Module (beside relay board)
    mcu_pcb = Pos(164.0, 15.0, -55.0) * Rot(Y=90) * Box(24.0, 50.0, 1.6)
    
    # 12V DC Power Supply Module (Lower rear right, at X = 136.0, Y = -58.0, Z = -95.0)
    psu_box = Pos(136.0, -58.0, -95.0) * Box(46.0, 34.0, 36.0)
    
    return [relay_board, mcu_pcb, psu_box]


# ==============================================================================
# 5. MASTER BUILD & EXPORT
# ==============================================================================
def build_all():
    print("Building KEF Peristaltic Pump...")
    single_pump = create_kef_pump_solid()
    pump_step_path = os.path.join(EXPORT_DIR, "kef_peristaltic_pump.step")
    export_step(single_pump, pump_step_path)
    print(f"Exported: {pump_step_path}")
    
    pump_xs = [-128.0, -64.0, 0.0, 64.0]
    pump_ys = [-30.0, 38.0]
    
    print("Building Solid Front Mounting Panel...")
    front_panel = create_front_panel(pump_xs, pump_ys)
    panel_step_path = os.path.join(EXPORT_DIR, "front_mounting_panel.step")
    export_step(front_panel, panel_step_path)
    print(f"Exported: {panel_step_path}")
    
    print("Building Chassis Enclosure...")
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
    
    print("Assembling External-Pumps Station Assembly...")
    # Pumps rest on the FRONT of the front panel (Z = 0)
    # Pump origin (back of flange) is at Z = 0
    pumps_assembly = []
    for py in pump_ys:
        for px in pump_xs:
            placed_pump = Pos(px, py, 0.0) * single_pump
            pumps_assembly.append(placed_pump)
            
    # Full Assembly (Front Panel + 8 External Pumps + Chassis + Electronics)
    full_assembly_parts = [
        chassis,
        front_panel,
    ] + elec_list + pumps_assembly
    
    full_assembly = Compound(full_assembly_parts)
    assembly_step_path = os.path.join(EXPORT_DIR, "8_channel_pump_station_assembly.step")
    export_step(full_assembly, assembly_step_path)
    print(f"Exported: {assembly_step_path}")
    
    # Internal view (without front panel, showing motors & electronics inside)
    internal_parts = [
        chassis,
    ] + elec_list + pumps_assembly
    internal_assembly = Compound(internal_parts)
    internal_step_path = os.path.join(EXPORT_DIR, "8_channel_pump_station_internal.step")
    export_step(internal_assembly, internal_step_path)
    print(f"Exported: {internal_step_path}")
    
    return {
        "pump": pump_step_path,
        "panel": panel_step_path,
        "chassis": chassis_step_path,
        "electronics": elec_step_path,
        "assembly": assembly_step_path,
        "internal": internal_step_path,
    }

if __name__ == "__main__":
    paths = build_all()
    print("All models successfully built and exported!")
