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
    Origin: center of the pump mounting flange FRONT face (Z = 0).
    Back face of flange is at Z = -4.0 mm.
    Z+ is forward (pump head), Z- is backward (motor).
    Y+ is up (nozzles point along +Y).
    X is horizontal (mounting ears extend along +/- X).
    """
    # 1. Flange (Z: -4.0 to 0)
    with BuildSketch() as sk_flange:
        Circle(radius=37.5 / 2)
        with Locations((-24.25, 0), (24.25, 0)):
            Circle(radius=4.05)
        Rectangle(48.5, 8.1)
        with Locations((-24.25, 0), (24.25, 0)):
            Circle(radius=3.2 / 2, mode=Mode.SUBTRACT)
    flange = Pos(0, 0, -2.0) * extrude(sk_flange.sketch, amount=2.0, both=True)
    
    # 2. Collar & Motor
    collar = Pos(0, 0, -9.7) * Cylinder(radius=31.5 / 2, height=11.6)
    motor = Pos(0, 0, -34.0) * Cylinder(radius=27.5 / 2, height=37.2)
    boss = Pos(0, 0, -53.5) * Cylinder(radius=7.0 / 2, height=2.2)
    t1 = Pos(-6.0, 0, -54.5) * Box(1.5, 3.5, 4.2)
    t2 = Pos(6.0, 0, -54.5) * Box(1.5, 3.5, 4.2)
    
    # 3. Pump Head Body (Z: 0 to 24.0)
    with BuildSketch() as sk_head:
        Circle(radius=37.5 / 2)
        with Locations((0, 14.5)):
            Rectangle(22.0, 14.7)  # Top manifold ridge up to Y = 21.85
    head_body = Pos(0, 0, 12.0) * extrude(sk_head.sketch, amount=12.1, both=True)
    
    # Front bezel ring & window
    rim = Pos(0, 0, 24.7) * extrude(Circle(radius=36.0 / 2) - Circle(radius=32.0 / 2), amount=0.8, both=True)
    win = Pos(0, 0, 24.4) * extrude(Circle(radius=31.5 / 2), amount=0.5, both=True)
    
    pump = flange + collar + motor + boss + t1 + t2 + head_body + rim + win
    
    # 4. Top Barbed Nozzles (Z = 17.0, X = +/- 6.5, Y > 21.85)
    for nx in [-6.5, 6.5]:
        nb = Pos(nx, 24.5, 17.0) * Rot(X=-90) * Cylinder(radius=4.0 / 2, height=6.5)
        b1 = Pos(nx, 29.5, 17.0) * Rot(X=-90) * Cone(bottom_radius=5.2 / 2, top_radius=3.8 / 2, height=4.2)
        b2 = Pos(nx, 33.5, 17.0) * Rot(X=-90) * Cone(bottom_radius=5.2 / 2, top_radius=3.8 / 2, height=4.2)
        nt = Pos(nx, 39.5, 17.0) * Rot(X=-90) * Cylinder(radius=3.5 / 2, height=8.2)
        pump = pump + nb + b1 + b2 + nt
        
    return pump


# ==============================================================================
# 2. PUMP MOUNTING PLATE (Single fused solid)
# ==============================================================================
def create_pump_mounting_plate(pump_xs, pump_ys, plate_front_z):
    """
    Creates the front mounting plate supporting the 8 peristaltic pumps.
    Front face of plate is at plate_front_z (Z = -35.0 mm).
    Back face is at plate_front_z - 4.0 = -39.0 mm.
    """
    plate_w = 264.0
    plate_h = 160.0
    plate_thick = 4.0
    
    plate_center_x = (pump_xs[0] + pump_xs[-1]) / 2.0  # -32.0 mm
    plate_center_y = (pump_ys[0] + pump_ys[-1]) / 2.0  # 4.0 mm
    
    with BuildSketch(Plane.XY.offset(plate_front_z - plate_thick)) as sk:
        with Locations((plate_center_x, plate_center_y)):
            RectangleRounded(plate_w, plate_h, radius=6.0)
            
        # 8 pump cutouts
        for py in pump_ys:
            for px in pump_xs:
                with Locations((px, py)):
                    # Central motor cutout dia 33.0 mm (Image 3 spec)
                    Circle(radius=33.0 / 2, mode=Mode.SUBTRACT)
                    # Two M3 mounting screw holes dia 3.2 mm at pitch 48.5 mm
                    with Locations((-24.25, 0), (24.25, 0)):
                        Circle(radius=3.2 / 2, mode=Mode.SUBTRACT)
                        
        # Cable / tubing pass-through slots below bottom row
        for px in pump_xs:
            with Locations((px, plate_center_y - 66.0)):
                SlotOverall(width=24.0, height=8.0, rotation=0, mode=Mode.SUBTRACT)
                
        # 4 mounting screw holes to chassis side tabs
        with Locations(
            (plate_center_x - plate_w / 2 + 8.0, plate_center_y - plate_h / 2 + 8.0),
            (plate_center_x - plate_w / 2 + 8.0, plate_center_y + plate_h / 2 - 8.0),
            (plate_center_x + plate_w / 2 - 8.0, plate_center_y - plate_h / 2 + 8.0),
            (plate_center_x + plate_w / 2 - 8.0, plate_center_y + plate_h / 2 - 8.0),
        ):
            Circle(radius=3.5 / 2, mode=Mode.SUBTRACT)
            
    plate = extrude(sk.sketch, amount=plate_thick, dir=(0, 0, 1))
    return plate


# ==============================================================================
# 3. CHASSIS ENCLOSURE (Single clean fused solid)
# ==============================================================================
def create_chassis_enclosure():
    """
    Creates the main 3D-printable unibody chassis.
    External dimensions: Width 352 mm, Height 176 mm, Depth 146 mm.
    Front outer bezel is at Z = 0.
    """
    W = 352.0
    H = 176.0
    D = 146.0
    WALL = 4.0
    
    # Outer box: Z from -D to 0
    with BuildSketch(Plane.XY.offset(-D)) as sk_outer:
        RectangleRounded(W, H, radius=14.0)
    outer = extrude(sk_outer.sketch, amount=D, dir=(0, 0, 1))
    
    # Inner void: Z from -D + WALL to 0
    with BuildSketch(Plane.XY.offset(-D + WALL)) as sk_inner:
        RectangleRounded(W - 2 * WALL, H - 2 * WALL, radius=10.0)
    inner = extrude(sk_inner.sketch, amount=D - WALL, dir=(0, 0, 1))
    
    body = outer - inner
    
    # Front bezel recess for acrylic window: Z from -3.2 to 0
    with BuildSketch(Plane.XY.offset(-3.2)) as sk_rec:
        RectangleRounded(338.0, 162.0, radius=10.0)
    recess = extrude(sk_rec.sketch, amount=3.2, dir=(0, 0, 1))
    body = body - recess
    
    # 4 Corner bosses for acrylic window
    bosses = []
    boss_holes = []
    for bx in [-158.0, 158.0]:
        for by in [-70.0, 70.0]:
            b = Pos(bx, by, -9.6) * Cylinder(radius=5.5, height=13.0)
            bh = Pos(bx, by, -8.0) * Cylinder(radius=3.2 / 2, height=16.0)
            bosses.append(b)
            boss_holes.append(bh)
            
    for b in bosses:
        body = body + b
    for bh in boss_holes:
        body = body - bh
        
    # 4 Bottom Foot Pads (with overlap into floor)
    feet = []
    for fx in [-148.0, 148.0]:
        for fz in [-D + 25.0, -25.0]:
            ft = Pos(fx, -H/2 - 3.0 + 0.25, fz) * Rot(X=90) * Cylinder(radius=10.0, height=6.5)
            feet.append(ft)
    for ft in feet:
        body = body + ft
        
    # Right Side Ventilation Slots (X = W/2 = 176 mm)
    # Upper horizontal slots along Z (rotation = 90)
    for sy in [28.0, 40.0, 52.0, 64.0]:
        slot = Pos(176.0, sy, -70.0) * Box(WALL * 2 + 2, 4.0, 34.0)
        body = body - slot
        
    # Lower vertical slots along Y (rotation = 0)
    for sz in [-105.0, -90.0, -75.0, -60.0]:
        slot = Pos(176.0, -35.0, sz) * Box(WALL * 2 + 2, 30.0, 4.0)
        body = body - slot
        
    # Rear DC power inlet hole at Z = -D
    dc_hole = Pos(135.0, -55.0, -D) * Cylinder(radius=6.0, height=WALL * 2 + 2)
    body = body - dc_hole
    
    # Internal middle partition wall at X = 104.0 mm
    partition = Pos(104.0, 0, -88.5) * Box(WALL, H - 2 * WALL, 107.0)
    wire_cutout = Pos(104.0, -20.0, -70.0) * Box(WALL + 2, 40.0, 30.0)
    body = body + (partition - wire_cutout)
    
    # Internal mounting tabs for pump plate at Z = -35.0 mm (behind plate)
    tab_left = Pos(-172.0 + 7.5, 0, -41.0) * Box(15.0, 140.0, 4.0)
    tab_mid = Pos(104.0 - 5.0, 0, -41.0) * Box(6.0, 140.0, 4.0)
    body = body + tab_left + tab_mid
    
    # Bottom front tubing exit slots
    for px in [-128.0, -64.0, 0.0, 64.0]:
        tube_slot = Pos(px, -H/2 + WALL/2, -18.0) * Box(20.0, WALL + 2, 8.0)
        body = body - tube_slot
        
    return body


# ==============================================================================
# 4. TRANSPARENT ACRYLIC FRONT COVER (Single solid)
# ==============================================================================
def create_acrylic_front_cover():
    """
    Creates the clear acrylic front faceplate.
    Dimensions: 336.0 x 160.0 x 3.0 mm.
    Z from -3.0 to 0.0 mm.
    """
    with BuildSketch(Plane.XY.offset(-3.0)) as sk:
        RectangleRounded(336.0, 160.0, radius=10.0)
        # 4 Corner mounting screw holes
        for bx in [-158.0, 158.0]:
            for by in [-70.0, 70.0]:
                with Locations((bx, by)):
                    Circle(radius=3.5 / 2, mode=Mode.SUBTRACT)
    cover = extrude(sk.sketch, amount=3.0, dir=(0, 0, 1))
    return cover


# ==============================================================================
# 5. ELECTRONIC MODULES (Clean fused solids)
# ==============================================================================
def create_electronic_modules():
    """
    Creates representative clean solids for:
    - 8-Channel Relay Board (vertical mounted)
    - 12V Power Supply Module
    - MCU / Control Board
    """
    # 8-Channel Relay Board (Vertical at X = 138.0, Z = -90.0)
    relay_board = Pos(138.0, 8.0, -90.0) * Box(50.0, 136.0, 1.6)
    for ry in range(8):
        pos_y = -48.0 + ry * 15.0
        relay_cube = Pos(130.0, pos_y, -81.7) * Box(15.0, 12.0, 15.0)
        relay_board = relay_board + relay_cube
    tb_top = Pos(138.0, 68.0, -84.2) * Box(46.0, 10.0, 10.0)
    tb_bot = Pos(138.0, -52.0, -84.2) * Box(46.0, 10.0, 10.0)
    relay_board = relay_board + tb_top + tb_bot
    
    # MCU Module
    mcu_pcb = Pos(164.0, 15.0, -70.0) * Rot(Y=90) * Box(24.0, 50.0, 1.6)
    
    # 12V DC Power Supply Module
    psu_box = Pos(138.0, -58.0, -118.0) * Box(46.0, 34.0, 36.0)
    
    return [relay_board, mcu_pcb, psu_box]


# ==============================================================================
# 6. FULL MASTER BUILD
# ==============================================================================
def build_all():
    print("Building KEF Peristaltic Pump...")
    single_pump = create_kef_pump_solid()
    pump_step_path = os.path.join(EXPORT_DIR, "kef_peristaltic_pump.step")
    export_step(single_pump, pump_step_path)
    print(f"Exported: {pump_step_path}")
    
    pump_xs = [-128.0, -64.0, 0.0, 64.0]
    pump_ys = [-30.0, 38.0]
    plate_front_z = -35.0
    
    print("Building Pump Mounting Plate...")
    mounting_plate = create_pump_mounting_plate(pump_xs, pump_ys, plate_front_z)
    plate_step_path = os.path.join(EXPORT_DIR, "pump_mounting_plate.step")
    export_step(mounting_plate, plate_step_path)
    print(f"Exported: {plate_step_path}")
    
    print("Building Chassis Enclosure...")
    chassis = create_chassis_enclosure()
    chassis_step_path = os.path.join(EXPORT_DIR, "chassis_enclosure.step")
    export_step(chassis, chassis_step_path)
    print(f"Exported: {chassis_step_path}")
    
    print("Building Transparent Front Cover...")
    acrylic_cover = create_acrylic_front_cover()
    acrylic_step_path = os.path.join(EXPORT_DIR, "transparent_front_cover.step")
    export_step(acrylic_cover, acrylic_step_path)
    print(f"Exported: {acrylic_step_path}")
    
    print("Building Electronic Modules...")
    elec_list = create_electronic_modules()
    elec_compound = Compound(elec_list)
    elec_step_path = os.path.join(EXPORT_DIR, "electronic_modules.step")
    export_step(elec_compound, elec_step_path)
    print(f"Exported: {elec_step_path}")
    
    print("Assembling Full 8-Channel Peristaltic Pump Station...")
    pump_mount_z = plate_front_z + 4.0
    pumps_assembly = []
    for py in pump_ys:
        for px in pump_xs:
            placed_pump = Pos(px, py, pump_mount_z) * single_pump
            pumps_assembly.append(placed_pump)
            
    full_assembly_parts = [
        chassis,
        mounting_plate,
        acrylic_cover,
    ] + elec_list + pumps_assembly
    
    full_assembly = Compound(full_assembly_parts)
    assembly_step_path = os.path.join(EXPORT_DIR, "8_channel_pump_station_assembly.step")
    export_step(full_assembly, assembly_step_path)
    print(f"Exported: {assembly_step_path}")
    
    internal_parts = [
        chassis,
        mounting_plate,
    ] + elec_list + pumps_assembly
    internal_assembly = Compound(internal_parts)
    internal_step_path = os.path.join(EXPORT_DIR, "8_channel_pump_station_internal.step")
    export_step(internal_assembly, internal_step_path)
    print(f"Exported: {internal_step_path}")
    
    return {
        "pump": pump_step_path,
        "plate": plate_step_path,
        "chassis": chassis_step_path,
        "acrylic": acrylic_step_path,
        "electronics": elec_step_path,
        "assembly": assembly_step_path,
        "internal": internal_step_path,
    }

if __name__ == "__main__":
    paths = build_all()
    print("All models successfully built and exported!")
