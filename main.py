import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import random, time, threading, pyautogui, keyboard, json, os

running = False
delay = 1.3
json_file = "numbers.json"
typed_count = 0

if os.path.exists(json_file):
    with open(json_file, "r") as f:
        typed_numbers = json.load(f)
else:
    typed_numbers = []

def save_numbers():
    with open(json_file, "w") as f:
        json.dump(typed_numbers, f)

def add_number_to_json(number):
    global typed_count
    if number not in typed_numbers:
        typed_numbers.append(number)
        typed_count += 1
        typed_counter.set(f"Numbers typed: {typed_count}")
        save_numbers()
        log_numbers(f"Typed: {number}")
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
    status_text.set("Running")

def stop_button():
    global running
    running = False
    status_text.set("Stopped")

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

keyboard.add_hotkey("ctrl+shift+t", toggle_running)

root = tk.Tk()
root.title("GusserV2")
root.geometry("750x650")
root.configure(bg="#000000")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background="#000000", borderwidth=0)
style.configure("TNotebook.Tab", background="#111111", foreground="#ffffff", padding=[10,5], font=("Arial", 11, "bold"))
style.map("TNotebook.Tab", background=[("selected","#ffffff")], foreground=[("selected","#000000")])

tabs = ttk.Notebook(root)
main_frame = tk.Frame(tabs, bg="#000000")
settings_frame = tk.Frame(tabs, bg="#000000")
tabs.add(main_frame, text="Main")
tabs.add(settings_frame, text="Settings")
tabs.pack(expand=True, fill="both")

def create_button(parent, text, command=None):
    btn = tk.Button(parent, text=text, command=command, fg="#ffffff", bg="#000000",
                    activeforeground="#000000", activebackground="#ffffff", bd=0, font=("Arial", 12, "bold"))
    btn.bind("<Enter>", lambda e: e.widget.config(bg="#ffffff", fg="#000000"))
    btn.bind("<Leave>", lambda e: e.widget.config(bg="#000000", fg="#ffffff"))
    return btn

def create_collapsible_frame(parent, title):
    container = tk.Frame(parent, bg="#111111")
    header = tk.Label(container, text=title, font=("Arial", 12, "bold"), fg="#ffffff", bg="#000000")
    header.pack(fill="x", pady=2)
    body = tk.Frame(container, bg="#222222")
    body.pack(fill="x")
    def toggle():
        if body.winfo_ismapped():
            body.pack_forget()
        else:
            body.pack(fill="x")
    header.bind("<Button-1>", lambda e: toggle())
    return container, body

title_label = tk.Label(main_frame, text="GusserV2", font=("Arial", 22, "bold"), fg="#ffffff", bg="#000000")
title_label.pack(pady=(15,10))

status_text = tk.StringVar(value="Stopped")
status_label = tk.Label(main_frame, textvariable=status_text, font=("Arial", 14, "bold"), fg="#ffffff", bg="#000000")
status_label.pack(pady=(0,5))

typed_counter = tk.StringVar(value=f"Numbers typed: {typed_count}")
typed_label = tk.Label(main_frame, textvariable=typed_counter, font=("Arial", 12), fg="#ffffff", bg="#000000")
typed_label.pack(pady=(0,5))

start_btn = create_button(main_frame, "Start", start_button)
stop_btn = create_button(main_frame, "Stop", stop_button)
clear_btn = create_button(main_frame, "Clear Database", clear_json)
reset_btn = create_button(main_frame, "Reset Count", reset_count)

for b in [start_btn, stop_btn, clear_btn, reset_btn]:
    b.pack(pady=5)

speed_label = tk.Label(main_frame, text="Typing Speed", font=("Arial", 12), fg="#ffffff", bg="#000000")
speed_label.pack(pady=(10,5))
speed_scale = tk.Scale(main_frame, from_=0.1, to=5.0, resolution=0.1, orient="horizontal",
                       command=update_speed, bg="#000000", fg="#ffffff", troughcolor="#555555",
                       highlightthickness=0, length=450)
speed_scale.set(delay)
speed_scale.pack(pady=5)

log_frame = tk.Frame(main_frame, bg="#000000")
log_frame.pack(pady=10, fill="both", expand=True)
log_scroll = tk.Scrollbar(log_frame)
log_scroll.pack(side="right", fill="y")
log_text = tk.Text(log_frame, bg="#111111", fg="#ffffff", state="disabled", yscrollcommand=log_scroll.set, font=("Consolas", 10))
log_text.pack(fill="both", expand=True)
log_scroll.config(command=log_text.yview)

general_frame, general_body = create_collapsible_frame(settings_frame, "General Settings")
general_frame.pack(fill="x", pady=5, padx=10)
bg_btn = create_button(general_body, "Background Color", lambda: root.configure(bg=colorchooser.askcolor()[1]))
fg_btn = create_button(general_body, "Text Color", lambda: title_label.config(fg=colorchooser.askcolor()[1]))
bg_btn.pack(pady=5)
fg_btn.pack(pady=5)

advanced_frame, advanced_body = create_collapsible_frame(settings_frame, "Advanced Settings")
advanced_frame.pack(fill="x", pady=5, padx=10)

def toggle_feature(name):
    log_numbers(f"{name} toggled")

feature_names = [
    "Button Background", "Button Text", "Random Number Range", "Auto Stop After X Numbers",
    "Enable Hotkey Toggle", "Auto Save", "Typing Delay Multiplier", "Shuffle Numbers Before Typing",
    "Enable Sound On Type", "Enable Visual Flash", "Extra Delay Between Types", "Enable Notifications",
    "Log To File", "Colorize Logs", "Keyboard Pause Detection", "Auto Clear Logs", "Custom Keybinds",
    "Show Tooltips", "Enable Multi-threading", "Enable Debug Mode"
]

for f in feature_names:
    chk = tk.Checkbutton(advanced_body, text=f, fg="#ffffff", bg="#222222", activebackground="#000000", activeforeground="#ffffff",
                         selectcolor="#000000", command=lambda name=f: toggle_feature(name))
    chk.pack(fill="x", pady=2, padx=5)

threading.Thread(target=typer_loop, daemon=True).start()
root.mainloop()


