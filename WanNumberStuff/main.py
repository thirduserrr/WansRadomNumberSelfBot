import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import random
import time
import threading
import pyautogui
import keyboard
import json
import os

running = False
delay = 1.3
json_file = "numbers.json"

if os.path.exists(json_file):
    with open(json_file, "r") as f:
        typed_numbers = json.load(f)
else:
    typed_numbers = []

def save_numbers():
    with open(json_file, "w") as f:
        json.dump(typed_numbers, f)

def add_number_to_json(number):
    if number not in typed_numbers:
        typed_numbers.append(number)
        save_numbers()
        return True
    return False

def clear_json():
    if messagebox.askyesno("Confirm", "Are you sure you want to clear the database?"):
        typed_numbers.clear()
        save_numbers()
        status_label.config(text="Database cleared!")

def toggle_running():
    global running
    running = not running
    update_status()

def update_status():
    if running:
        status_label.config(text="Status: Running", fg=app_fg)
    else:
        status_label.config(text="Status: Stopped", fg=app_fg)

def update_speed(val):
    global delay
    delay = float(val)

def typer_loop():
    global running
    while True:
        if running:
            num = random.randint(100, 500000)
            if add_number_to_json(num):
                pyautogui.typewrite(str(num))
                pyautogui.press("enter")
            time.sleep(delay)
        else:
            time.sleep(0.1)

def start_button():
    global running
    running = True
    update_status()

def stop_button():
    global running
    running = False
    update_status()

app_bg = "#000000"
app_fg = "#ffffff"
btn_bg = "#ffffff"
btn_fg = "#000000"

def choose_bg_color():
    global app_bg
    color = colorchooser.askcolor(title="Choose Background Color")[1]
    if color:
        app_bg = color
        root.configure(bg=app_bg)
        main_frame.configure(bg=app_bg)
        settings_frame.configure(bg=app_bg)
        update_widget_colors()

def choose_fg_color():
    global app_fg
    color = colorchooser.askcolor(title="Choose Text Color")[1]
    if color:
        app_fg = color
        update_widget_colors()

def choose_btn_bg_color():
    global btn_bg
    color = colorchooser.askcolor(title="Choose Button Background")[1]
    if color:
        btn_bg = color
        update_widget_colors()

def choose_btn_fg_color():
    global btn_fg
    color = colorchooser.askcolor(title="Choose Button Text")[1]
    if color:
        btn_fg = color
        update_widget_colors()

def update_widget_colors():
    status_label.config(fg=app_fg, bg=app_bg)
    title_label.config(fg=app_fg, bg=app_bg)
    speed_label.config(fg=app_fg, bg=app_bg)
    main_frame.config(bg=app_bg)
    settings_frame.config(bg=app_bg)
    for b in [start_btn, stop_btn, clear_btn, bg_btn, fg_btn, btn_bg_btn, btn_fg_btn]:
        b.config(bg=btn_bg, fg=btn_fg, activebackground=btn_fg, activeforeground=btn_bg, bd=0, relief="flat")

def on_enter(e):
    e.widget.config(bg=btn_fg, fg=btn_bg)

def on_leave(e):
    e.widget.config(bg=btn_bg, fg=btn_fg)

keyboard.add_hotkey('ctrl+shift+t', toggle_running)

root = tk.Tk()
root.title("Wans Number Guessing Bitch ass program")
root.geometry("500x400")
root.configure(bg=app_bg)

tabs = ttk.Notebook(root)
main_frame = tk.Frame(tabs, bg=app_bg)
settings_frame = tk.Frame(tabs, bg=app_bg)
tabs.add(main_frame, text="Main")
tabs.add(settings_frame, text="Settings")
tabs.pack(expand=True, fill="both")

title_label = tk.Label(main_frame, text="Wans Number Guessing Bitch ass program", font=("Arial", 16, "bold"), fg=app_fg, bg=app_bg)
title_label.pack(pady=(20,10))

status_label = tk.Label(main_frame, text="Status: turn it back on gng", font=("Arial", 13), fg=app_fg, bg=app_bg)
status_label.pack(pady=(0,15))

start_btn = tk.Button(main_frame, text="im on gng", width=20, command=start_button)
start_btn.pack(pady=6)
stop_btn = tk.Button(main_frame, text="stop abusing me", width=20, command=stop_button)
stop_btn.pack(pady=6)
clear_btn = tk.Button(main_frame, text="clear this shit", width=20, command=clear_json)
clear_btn.pack(pady=6)

speed_label = tk.Label(main_frame, text="goo brrr", font=("Arial", 12), fg=app_fg, bg=app_bg)
speed_label.pack(pady=(15,5))
speed_scale = tk.Scale(main_frame, from_=0.3, to=5.0, resolution=0.1, orient="horizontal", command=update_speed, bg=app_bg, fg=app_fg, troughcolor="#555555", highlightthickness=0)
speed_scale.set(delay)
speed_scale.pack(pady=5)

bg_btn = tk.Button(settings_frame, text="bg color", width=24, command=choose_bg_color)
bg_btn.pack(pady=10)
fg_btn = tk.Button(settings_frame, text="txt Color", width=24, command=choose_fg_color)
fg_btn.pack(pady=10)
btn_bg_btn = tk.Button(settings_frame, text="bttn background", width=24, command=choose_btn_bg_color)
btn_bg_btn.pack(pady=10)
btn_fg_btn = tk.Button(settings_frame, text="bttn txt", width=24, command=choose_btn_fg_color)
btn_fg_btn.pack(pady=10)

for b in [start_btn, stop_btn, clear_btn, bg_btn, fg_btn, btn_bg_btn, btn_fg_btn]:
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)

update_widget_colors()
threading.Thread(target=typer_loop, daemon=True).start()
root.mainloop()



