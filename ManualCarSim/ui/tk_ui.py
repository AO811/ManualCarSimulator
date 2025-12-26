import tkinter as tk
from tkinter import ttk
from simulator.state import CarState
from simulator.engine import update_state
from simulator. constants import MAX_RPM, REDLINE_RPM, IDLE_RPM

class SimulatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚗 Manual Driving Simulator")
        self.root.geometry("500x700")
        self.root.configure(bg="#1a1a2e")
        
        self.state = CarState()
        
        # Keyboard state
        self.keys = {
            'clutch': False,
            'brake': False,
            'accel': False
        }
        
        self.build_ui()
        self.bind_keys()
        self.update_loop()
    
    def build_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Title
        title = tk.Label(
            self.root, 
            text="🚗 Manual Driving Simulator", 
            font=("Arial", 18, "bold"),
            bg="#1a1a2e",
            fg="#eee"
        )
        title.pack(pady=10)
        
        # === Gauges Frame ===
        gauges_frame = tk.Frame(self.root, bg="#1a1a2e")
        gauges_frame.pack(pady=10)
        
        # RPM Gauge
        rpm_frame = tk.Frame(gauges_frame, bg="#1a1a2e")
        rpm_frame.pack(side="left", padx=20)
        
        tk.Label(rpm_frame, text="RPM", font=("Arial", 12), bg="#1a1a2e", fg="#aaa").pack()
        self.rpm_canvas = tk.Canvas(rpm_frame, width=120, height=120, bg="#1a1a2e", highlightthickness=0)
        self.rpm_canvas.pack()
        self.rpm_label = tk.Label(rpm_frame, text="800", font=("Arial", 20, "bold"), bg="#1a1a2e", fg="#0f0")
        self.rpm_label.pack()
        
        # Speed Gauge
        speed_frame = tk.Frame(gauges_frame, bg="#1a1a2e")
        speed_frame.pack(side="left", padx=20)
        
        tk.Label(speed_frame, text="SPEED", font=("Arial", 12), bg="#1a1a2e", fg="#aaa").pack()
        self.speed_canvas = tk.Canvas(speed_frame, width=120, height=120, bg="#1a1a2e", highlightthickness=0)
        self.speed_canvas.pack()
        self.speed_label = tk.Label(speed_frame, text="0 km/h", font=("Arial", 20, "bold"), bg="#1a1a2e", fg="#0ff")
        self.speed_label.pack()
        
        # === Gear Display ===
        gear_frame = tk.Frame(self.root, bg="#1a1a2e")
        gear_frame.pack(pady=15)
        
        tk.Label(gear_frame, text="GEAR", font=("Arial", 12), bg="#1a1a2e", fg="#aaa").pack()
        self.gear_display = tk.Label(gear_frame, text="N", font=("Arial", 48, "bold"), bg="#222", fg="#0f0", width=3)
        self.gear_display.pack()
        
        # Gear buttons
        gear_btn_frame = tk.Frame(self.root, bg="#1a1a2e")
        gear_btn_frame.pack(pady=5)
        
        self.gear_var = tk.IntVar(value=0)
        gears = [("R", -1), ("N", 0), ("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)]
        
        for text, value in gears:
            btn = tk.Radiobutton(
                gear_btn_frame, 
                text=text, 
                variable=self.gear_var, 
                value=value,
                font=("Arial", 12, "bold"),
                bg="#333",
                fg="#fff",
                selectcolor="#0a0",
                indicatoron=0,
                width=3,
                height=1
            )
            btn.pack(side="left", padx=2)
        
        # === Pedals Frame ===
        pedals_frame = tk.Frame(self. root, bg="#1a1a2e")
        pedals_frame.pack(pady=15)
        
        # Clutch
        clutch_frame = tk. Frame(pedals_frame, bg="#1a1a2e")
        clutch_frame.pack(side="left", padx=10)
        tk.Label(clutch_frame, text="CLUTCH [C]", font=("Arial", 10), bg="#1a1a2e", fg="#aaa").pack()
        self.clutch = tk.Scale(
            clutch_frame, from_=100, to=0, orient="vertical", 
            length=150, bg="#333", fg="#fff", troughcolor="#555",
            highlightthickness=0
        )
        self.clutch.set(0)  # Start with clutch pressed
        self.clutch.pack()
        
        # Brake
        brake_frame = tk.Frame(pedals_frame, bg="#1a1a2e")
        brake_frame.pack(side="left", padx=10)
        tk.Label(brake_frame, text="BRAKE [Space]", font=("Arial", 10), bg="#1a1a2e", fg="#aaa").pack()
        self.brake = tk.Scale(
            brake_frame, from_=100, to=0, orient="vertical",
            length=150, bg="#333", fg="#fff", troughcolor="#900",
            highlightthickness=0
        )
        self.brake.set(0)
        self.brake.pack()
        
        # Accelerator
        accel_frame = tk.Frame(pedals_frame, bg="#1a1a2e")
        accel_frame.pack(side="left", padx=10)
        tk.Label(accel_frame, text="GAS [↑]", font=("Arial", 10), bg="#1a1a2e", fg="#aaa").pack()
        self.accel = tk.Scale(
            accel_frame, from_=100, to=0, orient="vertical",
            length=150, bg="#333", fg="#fff", troughcolor="#090",
            highlightthickness=0
        )
        self.accel.set(0)
        self.accel.pack()
        
        # === Options Frame ===
        options_frame = tk.Frame(self.root, bg="#1a1a2e")
        options_frame. pack(pady=10)
        
        self.handbrake_var = tk.BooleanVar(value=False)
        self.handbrake_btn = tk.Checkbutton(
            options_frame, 
            text="🅿 Handbrake [H]", 
            variable=self.handbrake_var,
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="#fff",
            selectcolor="#900",
            activebackground="#1a1a2e"
        )
        self.handbrake_btn.pack(side="left", padx=10)
        
        self.hill_var = tk.BooleanVar(value=False)
        self.hill_btn = tk. Checkbutton(
            options_frame,
            text="⛰ Hill Mode",
            variable=self.hill_var,
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="#fff",
            selectcolor="#960",
            activebackground="#1a1a2e"
        )
        self.hill_btn.pack(side="left", padx=10)
        
        # === Feedback ===
        self.feedback = tk.Label(
            self. root, 
            text="🚗 Press C for clutch, shift to 1st, release slowly while adding gas! ",
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="#ff0",
            wraplength=450
        )
        self.feedback. pack(pady=15)
        
        # === Buttons ===
        btn_frame = tk.Frame(self.root, bg="#1a1a2e")
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame, 
            text="🔄 Reset Engine", 
            command=self.reset,
            font=("Arial", 11),
            bg="#333",
            fg="#fff"
        ).pack(side="left", padx=5)
        
        # === Controls Help ===
        help_text = "Keys:  C=Clutch | Space=Brake | ↑=Gas | 1-5=Gears | N=Neutral | R=Reverse | H=Handbrake"
        tk.Label(
            self.root,
            text=help_text,
            font=("Arial", 9),
            bg="#1a1a2e",
            fg="#666"
        ).pack(side="bottom", pady=5)
    
    def bind_keys(self):
        self.root.bind('<KeyPress-c>', lambda e: self.clutch. set(0))
        self.root.bind('<KeyRelease-c>', lambda e: self.clutch.set(100))
        self.root.bind('<KeyPress-space>', lambda e:  self.brake.set(100))
        self.root.bind('<KeyRelease-space>', lambda e: self.brake.set(0))
        self.root.bind('<KeyPress-Up>', lambda e: self.accel.set(100))
        self.root.bind('<KeyRelease-Up>', lambda e: self. accel.set(0))
        
        # Gear keys
        self.root.bind('1', lambda e: self.gear_var.set(1))
        self.root.bind('2', lambda e: self.gear_var.set(2))
        self.root.bind('3', lambda e: self.gear_var.set(3))
        self.root.bind('4', lambda e: self.gear_var. set(4))
        self.root.bind('5', lambda e: self.gear_var.set(5))
        self.root.bind('n', lambda e: self.gear_var.set(0))
        self.root.bind('r', lambda e: self.gear_var.set(-1))
        self.root.bind('h', lambda e: self.handbrake_var.set(not self.handbrake_var. get()))
    
    def reset(self):
        self.state. reset()
        self.clutch.set(0)
        self.brake.set(0)
        self.accel.set(0)
        self.gear_var.set(0)
        self.feedback.config(text="🔄 Engine restarted!  Ready to go.", fg="#0f0")
    
    def draw_rpm_gauge(self):
        self.rpm_canvas.delete("all")
        
        # Calculate fill percentage
        rpm_percent = min(self.state.rpm / MAX_RPM, 1.0)
        
        # Color based on RPM zone
        if self.state.rpm < 2000:
            color = "#00ff00"  # Green - low
        elif self.state.rpm < 4000:
            color = "#ffff00"  # Yellow - optimal
        elif self.state.rpm < REDLINE_RPM:
            color = "#ff9900"  # Orange - high
        else:
            color = "#ff0000"  # Red - redline
        
        # Draw arc background
        self.rpm_canvas. create_arc(10, 10, 110, 110, start=135, extent=270, style="arc", outline="#333", width=15)
        
        # Draw filled arc
        if rpm_percent > 0:
            extent = rpm_percent * 270
            self.rpm_canvas. create_arc(10, 10, 110, 110, start=135, extent=extent, style="arc", outline=color, width=15)
        
        self.rpm_label.config(text=f"{int(self.state.rpm)}", fg=color)
    
    def draw_speed_gauge(self):
        self.speed_canvas.delete("all")
        
        # Calculate fill percentage (max 180 km/h display)
        speed_percent = min(abs(self.state.speed) / 180, 1.0)
        
        color = "#00ffff"
        if self.state.speed < 0:
            color = "#ff6600"  # Orange for reverse
        
        # Draw arc background
        self.speed_canvas. create_arc(10, 10, 110, 110, start=135, extent=270, style="arc", outline="#333", width=15)
        
        # Draw filled arc
        if speed_percent > 0:
            extent = speed_percent * 270
            self.speed_canvas.create_arc(10, 10, 110, 110, start=135, extent=extent, style="arc", outline=color, width=15)
        
        speed_display = int(abs(self.state.speed))
        prefix = "-" if self.state.speed < 0 else ""
        self.speed_label.config(text=f"{prefix}{speed_display} km/h", fg=color)
    
    def update_gear_display(self):
        gear = self.gear_var.get()
        if gear == 0:
            text = "N"
            color = "#888"
        elif gear == -1:
            text = "R"
            color = "#f90"
        else:
            text = str(gear)
            color = "#0f0"
        
        self.gear_display. config(text=text, fg=color)
    
    def update_loop(self):
        # Update state from options
        self.state.handbrake = self.handbrake_var.get()
        self.state.on_hill = self.hill_var.get()
        
        # Run simulation
        msg = update_state(
            self.state,
            self.clutch.get(),
            self.accel.get(),
            self.brake.get(),
            self.gear_var.get()
        )
        
        # Update displays
        self.draw_rpm_gauge()
        self.draw_speed_gauge()
        self.update_gear_display()
        
        # Feedback color
        if "❌" in msg:
            fg_color = "#ff4444"
        elif "⚠" in msg:
            fg_color = "#ffaa00"
        elif "⬆" in msg or "⬇" in msg:
            fg_color = "#00aaff"
        elif "✔" in msg:
            fg_color = "#00ff00"
        else:
            fg_color = "#ffffff"
        
        self.feedback.config(text=msg, fg=fg_color)
        
        self.root.after(50, self.update_loop)  # 20 FPS for smoother updates