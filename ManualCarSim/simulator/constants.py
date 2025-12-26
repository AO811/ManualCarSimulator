# RPM Constants
IDLE_RPM = 800
MAX_RPM = 6500
STALL_RPM = 500
REDLINE_RPM = 6000

# Clutch Constants
CLUTCH_BITE_POINT = 30  # Clutch starts engaging at 30% released
CLUTCH_FULL_ENGAGE = 70  # Clutch fully engaged at 70% released

# Gear Ratios (affects acceleration and top speed per gear)
GEAR_RATIOS = {
    0: 0,      # Neutral
    1: 3.5,    # 1st gear - high torque, low speed
    2: 2.5,    # 2nd gear
    3: 1.8,    # 3rd gear
    4: 1.3,    # 4th gear
    5: 1.0,    # 5th gear - low torque, high speed
    -1: 3.5    # Reverse
}

# Speed limits per gear (km/h)
GEAR_MAX_SPEED = {
    0: 0,
    1: 30,
    2: 55,
    3: 85,
    4: 120,
    5: 180,
    -1: 20
}

# Optimal shift points (RPM)
OPTIMAL_SHIFT_UP_RPM = 3000
OPTIMAL_SHIFT_DOWN_RPM = 1500

# Physics factors
ACCEL_FACTOR = 0.15
BRAKE_FACTOR = 0.3
ENGINE_BRAKE_FACTOR = 0.05
RPM_DECAY_RATE = 50  # How fast RPM drops when not accelerating
SPEED_DECAY_RATE = 0.02  # Natural speed loss (friction/air resistance)

# Hill settings
HILL_INCLINE = 0.1  # Speed loss per update when on hill