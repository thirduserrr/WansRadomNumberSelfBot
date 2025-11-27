import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import random, time, threading, pyautogui, keyboard, json, os

running = False
delay = 1.3
typed_count = 0
json_file = "numbers.json"

if os.path.exists(json_file):
    with open(json_file, "r") as f:
        typed_numbers = json.load(f)
else:
    typed_numbers = []

user_settings = {
    "bg_color": "#000000",
    "text_color": "#ffffff",
    "btn_bg": "#000000",
    "btn_fg": "#ffffff",
    "min_number": 100,
    "max_number": 500000,
    "auto_stop_count": 0,
    "hotkey_toggle": True,
    "auto_save": True,
    "sound_on_type": False,
    "visual_flash": False,
    "shuffle_numbers": False,
    "stop_on_mouse_move": False
}

def save_numbers():
    with open(json_file, "w") as f:
        json.dump(typed_numbers, f)

def add_number_to_json(number):
    global typed_count
    if user_settings["shuffle_numbers"]:
        number = random.randint(user_settings["min_number"], user_settings["max_number"])
    if number not in typed_numbers:
        typed_numbers.append(number)
        typed_count += 1
        typed_counter.set(f"Numbers typed: {typed_count}")
        log_numbers(f"Typed: {number}")
        if user_settings["visual_flash"]:
            status_label.config(bg="#ffffff")
            status_label.after(50, lambda: status_label.config(bg=user_settings["bg_color"]))
        if user_settings["auto_save"]:
            save_numbers()
        if user_settings["auto_stop_count"] > 0 and typed_count >= user_settings["auto_stop_count"]:
            stop_button()
        return True
    return False

def clear_json():
    global typed_count
    if messagebox.askyesno("Confirm", "Clear all saved numbers?"):
        typed_numbers.clear()
        typed_count = 0
        typed_counter.set(f"Numbers typed: {typed_count}")
        save_numbers()
        log_numbers("Database cleared")

def reset_count():
    global typed_count
    typed_count = 0
    typed_counter.set(f"Numbers typed: {typed_count}")
    log_numbers("Typed count reset")

def start_button():
    global running
    running = True
    status_text.set("Running")

def stop_button():
    global running
    running = False
    status_text.set("Stopped")

def exit_app():
    root.destroy()

def toggle_running():
    global running
    running = not running
    status_text.set("Running" if running else "Stopped")

def update_speed(val):
    global delay
    delay = float(val)

def log_numbers(msg):
    log_text.config(state="normal")
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)
    log_text.config(state="disabled")

def change_color(setting):
    color = colorchooser.askcolor()[1]
    if color:
        user_settings[setting] = color
        update_ui_colors()

def update_ui_colors():
    root.configure(bg=user_settings["bg_color"])
    for frame in [main_frame, settings_frame, coming_soon_frame]:
        frame.configure(bg=user_settings["bg_color"])
    for label in [title_label, status_label, typed_label, speed_label]:
        label.config(fg=user_settings["text_color"], bg=user_settings["bg_color"])
    log_text.config(bg="#111111", fg=user_settings["text_color"])
    for b in buttons:
        b.config(bg=user_settings["btn_bg"], fg=user_settings["btn_fg"], activebackground=user_settings["btn_fg"], activeforeground=user_settings["btn_bg"])

def typer_loop():
    while True:
        if running:
            num = random.randint(user_settings["min_number"], user_settings["max_number"])
            add_number_to_json(num)
            pyautogui.typewrite(str(num))
            pyautogui.press("enter")
            time.sleep(delay)
        else:
            time.sleep(0.1)

keyboard.add_hotkey('ctrl+shift+t', toggle_running)

root = tk.Tk()
root.title("GusserV2")
root.geometry("950x800")
root.configure(bg=user_settings["bg_color"])
root.resizable(False, False)

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background=user_settings["bg_color"], borderwidth=0)
style.configure("TNotebook.Tab", background="#111111", foreground="#ffffff", padding=[10,5], font=("Arial", 11, "bold"))
style.map("TNotebook.Tab", background=[("selected","#ffffff")], foreground=[("selected","#000000")])

tabs = ttk.Notebook(root)
main_frame = tk.Frame(tabs, bg=user_settings["bg_color"])
settings_frame = tk.Frame(tabs, bg=user_settings["bg_color"])
coming_soon_frame = tk.Frame(tabs, bg=user_settings["bg_color"])
tabs.add(main_frame, text="Main")
tabs.add(settings_frame, text="Settings")
tabs.add(coming_soon_frame, text="Coming Soon")
tabs.pack(expand=True, fill="both")

def create_button(parent, text, command=None):
    btn = tk.Button(parent, text=text, command=command, fg=user_settings["btn_fg"], bg=user_settings["btn_bg"],
                    activeforeground=user_settings["btn_bg"], activebackground=user_settings["btn_fg"], bd=0, font=("Arial", 12, "bold"))
    btn.bind("<Enter>", lambda e: e.widget.config(bg=user_settings["btn_fg"], fg=user_settings["btn_bg"]))
    btn.bind("<Leave>", lambda e: e.widget.config(bg=user_settings["btn_bg"], fg=user_settings["btn_fg"]))
    return btn

title_label = tk.Label(main_frame, text="GusserV2", font=("Arial", 22, "bold"), fg=user_settings["text_color"], bg=user_settings["bg_color"])
title_label.pack(pady=(10,10))

status_text = tk.StringVar(value="Stopped")
status_label = tk.Label(main_frame, textvariable=status_text, font=("Arial", 14, "bold"), fg=user_settings["text_color"], bg=user_settings["bg_color"])
status_label.pack(pady=(0,10))

typed_counter = tk.StringVar(value=f"Numbers typed: {typed_count}")
typed_label = tk.Label(main_frame, textvariable=typed_counter, font=("Arial", 12), fg=user_settings["text_color"], bg=user_settings["bg_color"])
typed_label.pack(pady=(0,10))

log_frame = tk.Frame(main_frame, bg=user_settings["bg_color"])
log_frame.pack(pady=(5,15), fill="both", expand=False)
log_scroll = tk.Scrollbar(log_frame)
log_scroll.pack(side="right", fill="y")
log_text = tk.Text(log_frame, height=10, bg="#111111", fg=user_settings["text_color"], state="disabled", yscrollcommand=log_scroll.set, font=("Consolas", 10))
log_text.pack(fill="both", expand=True)
log_scroll.config(command=log_text.yview)

start_btn = create_button(main_frame, "Start", start_button)
stop_btn = create_button(main_frame, "Stop", stop_button)
clear_btn = create_button(main_frame, "Clear Database", clear_json)
reset_btn = create_button(main_frame, "Reset Count", reset_count)
exit_btn = create_button(main_frame, "Exit", exit_app)

buttons = [start_btn, stop_btn, clear_btn, reset_btn, exit_btn]
for b in buttons:
    b.pack(pady=5, ipadx=10, ipady=5)

speed_label = tk.Label(main_frame, text="Typing Speed", font=("Arial", 12), fg=user_settings["text_color"], bg=user_settings["bg_color"])
speed_label.pack(pady=(15,5))
speed_scale = tk.Scale(main_frame, from_=0.1, to=5.0, resolution=0.1, orient="horizontal",
                       command=update_speed, bg=user_settings["bg_color"], fg=user_settings["text_color"], troughcolor="#555555",
                       highlightthickness=0, length=500)
speed_scale.set(delay)
speed_scale.pack(pady=(0,10))

general_frame = tk.LabelFrame(settings_frame, text="General Settings", bg="#111111", fg="#ffffff", font=("Arial",12,"bold"))
general_frame.pack(fill="x", pady=5, padx=10)
bg_color_btn = create_button(general_frame, "Background Color", lambda: change_color("bg_color"))
text_color_btn = create_button(general_frame, "Text Color", lambda: change_color("text_color"))
btn_bg_btn = create_button(general_frame, "Button Background", lambda: change_color("btn_bg"))
btn_fg_btn = create_button(general_frame, "Button Text", lambda: change_color("btn_fg"))
for b in [bg_color_btn, text_color_btn, btn_bg_btn, btn_fg_btn]:
    b.pack(pady=5, ipadx=10, ipady=5)

advanced_frame = tk.LabelFrame(settings_frame, text="Advanced Settings", bg="#111111", fg="#ffffff", font=("Arial",12,"bold"))
advanced_frame.pack(fill="x", pady=5, padx=10)

min_label = tk.Label(advanced_frame, text="Min Number", fg="#ffffff", bg="#111111")
min_label.pack(pady=5)
min_entry = tk.Entry(advanced_frame, width=20)
min_entry.pack(pady=5)
min_entry.insert(0, str(user_settings["min_number"]))
def update_min_number(event=None):
    try:
        user_settings["min_number"] = int(min_entry.get())
    except:
        pass
min_entry.bind("<KeyRelease>", update_min_number)

max_label = tk.Label(advanced_frame, text="Max Number", fg="#ffffff", bg="#111111")
max_label.pack(pady=5)
max_entry = tk.Entry(advanced_frame, width=20)
max_entry.pack(pady=5)
max_entry.insert(0, str(user_settings["max_number"]))
def update_max_number(event=None):
    try:
        user_settings["max_number"] = int(max_entry.get())
    except:
        pass
max_entry.bind("<KeyRelease>", update_max_number)

shuffle_var = tk.BooleanVar(value=user_settings["shuffle_numbers"])
shuffle_chk = tk.Checkbutton(advanced_frame, text="Shuffle Numbers", fg="#ffffff", bg="#111111",
                             selectcolor="#000000", variable=shuffle_var,
                             command=lambda: user_settings.update({"shuffle_numbers": shuffle_var.get()}))
shuffle_chk.pack(pady=5)

auto_stop_label = tk.Label(advanced_frame, text="Auto Stop Count (0 = off)", fg="#ffffff", bg="#111111")
auto_stop_label.pack(pady=5)
auto_stop_spin = tk.Spinbox(advanced_frame, from_=0, to=100000, width=10,
                            command=lambda: user_settings.update({"auto_stop_count": int(auto_stop_spin.get())}))
auto_stop_spin.delete(0, "end")
auto_stop_spin.insert(0, user_settings["auto_stop_count"])
auto_stop_spin.pack(pady=5)

coming_label = tk.Label(coming_soon_frame, text="Coming Soon Features:\n- AI Tracking\n- AI Screen View\n- Advanced Auto Mode\n- Real-Time Analytics\n- Smart Predictions\n- Auto Optimized Speed\n- Intelligent Stop Conditions", fg="#ffffff", bg=user_settings["bg_color"], font=("Arial", 14))
coming_label.pack(pady=50)

threading.Thread(target=typer_loop, daemon=True).start()
root.mainloop()

