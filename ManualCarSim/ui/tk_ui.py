import tkinter as tk
from simulator.state import CarState
from simulator.engine import update_state

class SimulatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Manual Driving Simulator v1")

        self.state = CarState()

        self.build_ui()
        self.update_loop()

    def build_ui(self):
        tk.Label(self.root, text="Clutch").pack()
        self.clutch = tk.Scale(self.root, from_=0, to=100, orient="horizontal")
        self.clutch.set(100)
        self.clutch.pack()

        tk.Label(self.root, text="Accelerator").pack()
        self.accel = tk.Scale(self.root, from_=0, to=100, orient="horizontal")
        self.accel.pack()

        tk.Label(self.root, text="Brake").pack()
        self.brake = tk.Scale(self.root, from_=0, to=100, orient="horizontal")
        self.brake.pack()

        tk.Label(self.root, text="Gear").pack()
        self.gear = tk.IntVar(value=0)
        tk.OptionMenu(self.root, self.gear, 0, 1, 2, 3, 4, 5).pack()

        self.rpm_label = tk.Label(self.root, text="RPM: 800", font=("Arial", 14))
        self.rpm_label.pack()

        self.speed_label = tk.Label(self.root, text="Speed: 0 km/h", font=("Arial", 14))
        self.speed_label.pack()

        self.feedback = tk.Label(self.root, text="Ready", fg="blue")
        self.feedback.pack()

        tk.Button(self.root, text="Reset Engine", command=self.reset).pack()

    def reset(self):
        self.state.reset()
        self.feedback.config(text="Engine restarted")

    def update_loop(self):
        msg = update_state(
            self.state,
            self.clutch.get(),
            self.accel.get(),
            self.brake.get(),
            self.gear.get()
        )

        self.rpm_label.config(text=f"RPM: {int(self.state.rpm)}")
        self.speed_label.config(text=f"Speed: {int(self.state.speed)} km/h")
        self.feedback.config(text=msg)

        self.root.after(100, self.update_loop)
