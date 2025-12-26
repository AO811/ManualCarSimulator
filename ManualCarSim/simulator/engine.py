from simulator.constants import *

def update_state(state, clutch, accel, brake, gear):
    feedback = "✔ Driving..."

    if not state.engine_on:
        return "❌ Engine stalled. Press reset."

    state.gear = gear

    if clutch > 80 or gear == 0:
        state.rpm = IDLE_RPM + accel * ACCEL_RPM_FACTOR
        state.speed -= brake * ACCEL_SPEED_FACTOR
    else:
        load = gear * 15

        state.rpm = max(
            IDLE_RPM,
            state.rpm + accel * 6 - load
        )

        state.speed += (state.rpm / 3000) * gear * 0.05
        state.speed -= brake * BRAKE_SPEED_FACTOR

    if state.rpm < STALL_RPM:
        state.engine_on = False
        state.rpm = 0
        state.speed = 0
        return "❌ Car stalled!"

    state.rpm = min(state.rpm, MAX_RPM)
    state.speed = max(state.speed, 0)

    if state.rpm > 3000 and gear < 5:
        feedback = "⚠ Consider shifting up"
    if state.speed < 10 and gear >= 3:
        feedback = "⚠ Wrong gear for speed"

    return feedback
