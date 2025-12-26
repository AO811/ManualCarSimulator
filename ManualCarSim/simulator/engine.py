from simulator.constants import *

def get_clutch_engagement(clutch_pedal):
    """
    Calculate clutch engagement (0 to 1).
    clutch_pedal: 0 = fully released (engaged), 100 = fully pressed (disengaged)
    
    We need to INVERT the value since: 
    - Slider at 100 (top) = pedal pressed = disengaged = 0 engagement
    - Slider at 0 (bottom) = pedal released = engaged = 1 engagement
    """
    # Invert the clutch pedal value
    clutch_released = 100 - clutch_pedal
    
    if clutch_released >= CLUTCH_FULL_ENGAGE:
        return 1.0
    elif clutch_released <= CLUTCH_BITE_POINT:
        return 0.0
    else:
        # Gradual engagement between bite point and full engage
        return (clutch_released - CLUTCH_BITE_POINT) / (CLUTCH_FULL_ENGAGE - CLUTCH_BITE_POINT)
    
def update_state(state, clutch, accel, brake, gear):
    """
    Update car state based on inputs.
    clutch: 0 = pressed (disengaged), 100 = released (engaged)
    accel: 0-100 accelerator pedal
    brake: 0-100 brake pedal
    gear: -1 (R), 0 (N), 1-5
    """
    if not state.engine_on:
        return "❌ Engine stalled!  Press Reset to restart."
    
    state.gear = gear
    engagement = get_clutch_engagement(clutch)
    
    feedback = "✔ Ready"
    
    # --- Handbrake logic ---
    if state.handbrake:
        if state.speed > 0:
            state. speed = max(0, state.speed - BRAKE_FACTOR * 2)
        feedback = "🅿 Handbrake engaged"
    
    # --- Neutral or clutch fully pressed ---
    if gear == 0 or engagement == 0:
        # Engine revs freely
        target_rpm = IDLE_RPM + (accel / 100) * (MAX_RPM - IDLE_RPM) * 0.6
        state.rpm += (target_rpm - state.rpm) * 0.1
        
        # Apply brakes or natural slowdown
        if brake > 0:
            state. speed = max(0, state. speed - brake / 100 * BRAKE_FACTOR)
        else:
            state.speed = max(0, state.speed - SPEED_DECAY_RATE)
        
        # Hill rollback
        if state.on_hill and not state.handbrake and state.speed == 0:
            feedback = "⚠ Car rolling back!  Use handbrake!"
        
        if gear == 0:
            feedback = "🔄 In Neutral" if feedback == "✔ Ready" else feedback
        else:
            feedback = "🦶 Clutch pressed" if feedback == "✔ Ready" else feedback
    
    # --- Gear engaged with clutch (partially) released ---
    else:
        gear_ratio = GEAR_RATIOS. get(gear, 1)
        max_speed = GEAR_MAX_SPEED.get(gear, 100)
        
        # Calculate engine load based on speed and gear
        if state.speed > 0:
            wheel_rpm = (state.speed / max_speed) * REDLINE_RPM
        else: 
            wheel_rpm = IDLE_RPM
        
        # Blend between engine RPM and wheel RPM based on clutch engagement
        target_rpm = (1 - engagement) * state.rpm + engagement * wheel_rpm
        
        # Add acceleration
        if accel > 0:
            rpm_increase = (accel / 100) * 500 * gear_ratio
            target_rpm += rpm_increase
        
        # Smooth RPM transition
        state.rpm += (target_rpm - state.rpm) * 0.15
        
        # --- Stall detection ---
        # Stall if RPM drops too low when clutch is engaged
        if state.rpm < STALL_RPM and engagement > 0.5:
            state.stall()
            return "❌ Car stalled!  Released clutch too fast without enough gas."
        
        # --- Speed calculation ---
        if not state.handbrake:
            # Power to wheels
            power = (state.rpm - IDLE_RPM) / (MAX_RPM - IDLE_RPM)
            acceleration = power * ACCEL_FACTOR * gear_ratio * engagement
            
            # Reverse gear
            if gear == -1:
                state.speed = max(-GEAR_MAX_SPEED[-1], min(0, state.speed - acceleration))
            else:
                state.speed += acceleration
            
            # Speed cap per gear
            if gear > 0:
                state.speed = min(state.speed, max_speed)
            
            # Braking
            if brake > 0:
                brake_power = (brake / 100) * BRAKE_FACTOR
                if state.speed > 0:
                    state.speed = max(0, state.speed - brake_power)
                elif state.speed < 0:
                    state.speed = min(0, state.speed + brake_power)
            
            # Engine braking (when not accelerating)
            if accel == 0 and state.speed > 0:
                state.speed = max(0, state.speed - ENGINE_BRAKE_FACTOR * gear_ratio)
            
            # Hill effect
            if state.on_hill and state.speed < 5 and gear > 0:
                state.speed = max(0, state.speed - HILL_INCLINE)
                if state.speed == 0 and accel < 30:
                    feedback = "⚠ Need more gas on hill!"
        
        # --- Feedback ---
        if feedback == "✔ Ready":
            feedback = "✔ Driving..."
        
        # Shift suggestions
        if state.rpm > OPTIMAL_SHIFT_UP_RPM and gear < 5 and gear > 0:
            feedback = f"⬆ Shift up!  RPM high for gear {gear}"
        elif state.rpm < OPTIMAL_SHIFT_DOWN_RPM and gear > 1 and state.speed > 10:
            feedback = f"⬇ Shift down! RPM low for gear {gear}"
        
        # Redline warning
        if state.rpm > REDLINE_RPM: 
            state.rpm = REDLINE_RPM
            feedback = "🔴 REDLINE!  Shift up or ease off!"
        
        # Wrong gear warnings
        if state.speed < 10 and gear >= 3:
            feedback = "⚠ Gear too high for speed!"
        if state.speed > GEAR_MAX_SPEED. get(gear, 100) * 0.95 and gear < 5:
            feedback = f"⬆ Maxed out gear {gear}!  Shift up!"
    
    # Clamp values
    state.rpm = max(0, min(state.rpm, MAX_RPM))
    state.speed = max(-GEAR_MAX_SPEED.get(-1, 20), state.speed)
    
    return feedback