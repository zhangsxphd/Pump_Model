import math
from build123d import *

# ==========================================
# PARAMETERS & DIMENSIONS (All in mm)
# ==========================================

# KEF Pump Dimensions (from Kamoer engineering drawing)
PUMP_FLANGE_W = 56.6
PUMP_EAR_HOLE_PITCH = 48.5
PUMP_EAR_HOLE_DIA = 3.2
PUMP_BODY_DIA = 37.5
PUMP_HEAD_HEIGHT = 40.6
PUMP_HEAD_DEPTH = 24.0
PUMP_COLLAR_DIA = 31.5
PUMP_COLLAR_LEN = 11.5
PUMP_MOTOR_DIA = 27.5
PUMP_MOTOR_LEN = 37.0
PUMP_TOTAL_LEN = 80.5
PUMP_CUTOUT_DIA = 33.0  # Cutout on mounting plate

# Layout of 8 Pumps (2 rows x 4)
PUMP_PITCH_X = 66.0      # Horizontal spacing between pump centers
PUMP_PITCH_Y = 68.0      # Vertical spacing between rows
PUMP_X_START = - (3 * PUMP_PITCH_X) / 2  # Centered about pump bay

# Mounting Plate Dimensions
PLATE_THICKNESS = 4.0
PLATE_W = 280.0
PLATE_H = 160.0

# Chassis Internal Dimensions
INTERIOR_W = 350.0       # Left to right
INTERIOR_H = 168.0       # Floor to ceiling
INTERIOR_D = 145.0       # Inside front to inside back
WALL = 4.0               # Chassis wall thickness

OUTER_W = INTERIOR_W + 2 * WALL  # 358 mm
OUTER_H = INTERIOR_H + 2 * WALL  # 176 mm
OUTER_D = INTERIOR_D + WALL      # 149 mm (+ front bezel)

print(f"Chassis outer: {OUTER_W} x {OUTER_H} x {OUTER_D} mm")
