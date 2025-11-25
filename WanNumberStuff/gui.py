import tkinter as tk
from tkinter import ttk, messagebox
import threading
import keyboard
from typer_logic import typer_loop, running, delay, clear_numbers
from settings import app_bg, app_fg, btn_bg, btn_fg, choose_bg_color, choose_fg_color, choose_btn_bg_color, choose_btn_fg_color

class WansTyperApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wans Number Guessing Bitch ass program")
        self.root.geometry("500x400")
        self.root.configure(bg=app_bg)
        self.setup_gui()
        keyboard.add_hotkey('ctrl+shift+t', self.toggle_running)
        threading.Thread(target=typer_loop, daemon=True).start()

    def setup_gui(self):
        self.tabs = ttk.Notebook(self.root)
        self.main_frame = tk.Frame(self.tabs, bg=app_bg)
        self.settings_frame = tk.Frame(self.tabs, bg=app_bg)
        self.tabs.add(self.main_frame, text="Main")
        self.tabs.add(self.settings_frame, text="Settings")
        self.tabs.pack(expand=True, fill="both")

        self.title_label = tk.Label(self.main_frame, text="Wans Number Guessing Bitch ass program", font=("Arial",16,"bold"), fg=app_fg, bg=app_bg)
        self.title_label.pack(pady=(20,10))

        self.status_label = tk.Label(self.main_frame, text="Status: turn it back on gng", font=("Arial",13), fg=app_fg, bg=app_bg)
        self.status_label.pack(pady=(0,15))

        self.start_btn = tk.Button(self.main_frame, text="im on gng", width=20, command=self.start)
        self.start_btn.pack(pady=6)
        self.stop_btn = tk.Button(self.main_frame, text="stop abusing me", width=20, command=self.stop)
        self.stop_btn.pack(pady=6)
        self.clear_btn = tk.Button(self.main_frame, text="clear this shit", width=20, command=self.clear_db)
        self.clear_btn.pack(pady=6)

        self.speed_label = tk.Label(self.main_frame, text="goo brrr", font=("Arial",12), fg=app_fg, bg=app_bg)
        self.speed_label.pack(pady=(15,5))
        self.speed_scale = tk.Scale(self.main_frame, from_=0.3, to=5.0, resolution=0.1, orient="horizontal", command=self.update_speed, bg=app_bg, fg=app_fg, troughcolor="#555555", highlightthickness=0)
        self.speed_scale.set(delay)
        self.speed_scale.pack(pady=5)

        self.bg_btn = tk.Button(self.settings_frame, text="bg color", width=24, command=lambda: choose_bg_color(self.root, self.main_frame, self.settings_frame, self.update_widget_colors))
        self.bg_btn.pack(pady=10)
        self.fg_btn = tk.Button(self.settings_frame, text="txt Color", width=24, command=lambda: choose_fg_color(self.update_widget_colors))
        self.fg_btn.pack(pady=10)
        self.btn_bg_btn = tk.Button(self.settings_frame, text="bttn background", width=24, command=lambda: choose_btn_bg_color(self.update_widget_colors))
        self.btn_bg_btn.pack(pady=10)
        self.btn_fg_btn = tk.Button(self.settings_frame, text="bttn txt", width=24, command=lambda: choose_btn_fg_color(self.update_widget_colors))
        self.btn_fg_btn.pack(pady=10)

        for b in [self.start_btn, self.stop_btn, self.clear_btn, self.bg_btn, self.fg_btn, self.btn_bg_btn, self.btn_fg_btn]:
            b.bind("<Enter>", self.on_enter)
            b.bind("<Leave>", self.on_leave)

        self.update_widget_colors()

    def update_widget_colors(self):
        self.status_label.config(fg=app_fg, bg=app_bg)
        self.title_label.config(fg=app_fg, bg=app_bg)
        self.speed_label.config(fg=app_fg, bg=app_bg)
        self.main_frame.config(bg=app_bg)
        self.settings_frame.config(bg=app_bg)
        for b in [self.start_btn, self.stop_btn, self.clear_btn, self.bg_btn, self.fg_btn, self.btn_bg_btn, self.btn_fg_btn]:
            b.config(bg=btn_bg, fg=btn_fg, activebackground=btn_fg, activeforeground=btn_bg, bd=0, relief="flat")

    def on_enter(self, e):
        e.widget.config(bg=btn_fg, fg=btn_bg)

    def on_leave(self, e):
        e.widget.config(bg=btn_bg, fg=btn_fg)

    def toggle_running(self):
        global running
        running = not running
        self.update_status()

    def update_status(self):
        if running:
            self.status_label.config(text="Status: Running", fg=app_fg)
        else:
            self.status_label.config(text="Status: Stopped", fg=app_fg)

    def start(self):
        global running
        running = True
        self.update_status()

    def stop(self):
        global running
        running = False
        self.update_status()

    def clear_db(self):
        clear_numbers()
        self.status_label.config(text="Database cleared!")

    def update_speed(self, val):
        global delay
        delay = float(val)

    def run(self):
        self.root.mainloop()
