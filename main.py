import tkinter as tk
from tkinter import messagebox
import json, os, threading, time, random, traceback
import pyautogui
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

DB_FILE = "numbers.json"
if os.path.exists(DB_FILE):
    with open(DB_FILE,"r") as f:
        numbers_db = json.load(f)
else:
    numbers_db = []

state = {
    "running": False,
    "typed_count": len(numbers_db),
    "typed_chars": sum(len(str(n)) for n in numbers_db),
    "min_number": 100,
    "max_number": 500000,
    "delay": 1.0,
    "shuffle_numbers": False,
    "auto_save": True,
    "enable_ai_panel": True,
    "theme": "dark"
}

THEME = {
    "bg":"#121212",
    "panel":"#1c1c1c",
    "glass":"#1e1e1e",
    "text":"#ffffff",
    "accent":"#56CCF2",
    "btn_grad_start":"#56CCF2",
    "btn_grad_end":"#2F80ED",
    "hover":"#3aa0f2"
}

def log_error(e):
    with open("gusserv3_errors.log","a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {str(e)}\n")
        f.write(traceback.format_exc()+"\n")

def save_db():
    try:
        with open(DB_FILE,"w") as f:
            json.dump(numbers_db,f)
    except Exception as e:
        log_error(e)

nn_model = Sequential()
nn_model.add(Dense(32,input_dim=5,activation='relu'))
nn_model.add(Dense(16,activation='relu'))
nn_model.add(Dense(1,activation='linear'))
nn_model.compile(optimizer=Adam(0.01),loss='mse')

def train_model():
    try:
        if len(numbers_db)<10:
            return
        X,y=[],[]
        for i in range(len(numbers_db)-5):
            X.append(numbers_db[i:i+5])
            y.append(numbers_db[i+5])
        X,y=np.array(X),np.array(y)
        nn_model.fit(X,y,epochs=5,verbose=0)
    except Exception as e:
        log_error(e)

def predict_next():
    try:
        if len(numbers_db)<5:
            return numbers_db[-1] if numbers_db else 0
        last=np.array(numbers_db[-5:]).reshape(1,-1)
        pred=nn_model.predict(last,verbose=0)
        return int(pred[0][0])
    except Exception as e:
        log_error(e)
        return 0

root=tk.Tk()
root.withdraw()
splash=tk.Toplevel()
splash.geometry("500x250+600+300")
splash.configure(bg=THEME["panel"])
tk.Label(splash,text="Loading Gusser V3",font=("Segoe UI",18,"bold"),bg=THEME["panel"],fg=THEME["accent"]).pack(expand=True)
root.after(2000, lambda: (splash.destroy(), root.deiconify()))

root.title("GusserV3 Ultra")
root.geometry("1120x760")
root.configure(bg=THEME["bg"])

topbar=tk.Frame(root,bg=THEME["panel"],height=64)
topbar.pack(side="top",fill="x")
title=tk.Label(topbar,text="GusserV3 Ultra",fg=THEME["accent"],bg=THEME["panel"],font=("Segoe UI",18,"bold"))
title.pack(side="left",padx=12,pady=10)

content_frames={}
for name in ("Numbers","Settings","Updates"):
    f=tk.Frame(root,bg=THEME["bg"])
    f.place(x=0,y=64,relwidth=1,relheight=1,height=-64)
    content_frames[name]=f

def show(name):
    for k,v in content_frames.items():
        v.place_forget()
    content_frames[name].place(x=0,y=64,relwidth=1,relheight=1,height=-64)

def make_tab_button(text,cmd):
    b=tk.Button(topbar,text=text,command=cmd,fg=THEME["text"],bg=THEME["panel"],bd=0,font=("Segoe UI",11,"bold"))
    b.pack(side="left",padx=10)
    return b

make_tab_button("Home",lambda: show("Numbers"))
make_tab_button("Settings",lambda: show("Settings"))
make_tab_button("Updates",lambda: show("Updates"))
exit_btn=tk.Button(topbar,text="Exit",command=root.destroy,fg=THEME["text"],bg=THEME["panel"],bd=0,font=("Segoe UI",11,"bold"))
exit_btn.pack(side="right",padx=12)

typed_counter=tk.StringVar(value=f"Numbers: {state['typed_count']} | Chars: {state['typed_chars']}")
tk.Label(content_frames["Numbers"],textvariable=typed_counter,font=("Segoe UI",16,"bold"),fg=THEME["accent"],bg=THEME["bg"]).pack(pady=8)

number_log_frame=tk.Frame(content_frames["Numbers"],bg=THEME["bg"])
number_log_frame.pack(pady=5,fill="both",expand=True)
num_scroll=tk.Scrollbar(number_log_frame)
num_scroll.pack(side="right",fill="y")
number_log=tk.Text(number_log_frame,height=15,bg=THEME["glass"],fg=THEME["text"],state="disabled",yscrollcommand=num_scroll.set,font=("Consolas",11))
number_log.pack(fill="both",expand=True)
num_scroll.config(command=number_log.yview)

control_frame=tk.Frame(content_frames["Numbers"],bg=THEME["bg"])
control_frame.pack(pady=10)

def create_gradient_button(parent,text,command):
    b=tk.Button(parent,text=text,fg="white",font=("Segoe UI",12,"bold"),command=command,bd=0,relief="flat",bg=THEME["btn_grad_start"],activebackground=THEME["btn_grad_end"])
    b.bind("<Enter>",lambda e:b.config(bg=THEME["hover"]))
    b.bind("<Leave>",lambda e:b.config(bg=THEME["btn_grad_start"]))
    return b

ai_panel=None
ai_pred_label=None

def safe_update_label(label,text):
    try:
        if label and label.winfo_exists():
            label.after(0,lambda: label.config(text=text))
    except Exception as e:
        log_error(e)

def open_ai_panel():
    global ai_panel,ai_pred_label
    try:
        if not state["enable_ai_panel"]:
            return
        if ai_panel and ai_panel.winfo_exists():
            ai_panel.deiconify()
            return
        ai_panel=tk.Toplevel(root)
        ai_panel.title("AI Panel")
        ai_panel.geometry("320x180+900+120")
        ai_panel.configure(bg=THEME["panel"])
        ai_panel.attributes("-topmost",True)
        tk.Label(ai_panel,text="AI Prediction Panel",bg=THEME["panel"],fg=THEME["accent"],font=("Segoe UI",13,"bold")).pack(pady=8)
        ai_pred_label=tk.Label(ai_panel,text="Predicted: —",bg=THEME["panel"],fg=THEME["text"],font=("Segoe UI",12))
        ai_pred_label.pack(pady=6)
        tk.Button(ai_panel,text="Hide",command=lambda: ai_panel.withdraw(),bg=THEME["panel"],fg=THEME["text"]).pack(pady=10)
    except Exception as e:
        log_error(e)

def update_ai_prediction():
    if ai_pred_label:
        safe_update_label(ai_pred_label,f"Predicted: {predict_next()}")

def number_log_update(n):
    try:
        number_log.config(state="normal")
        number_log.insert(tk.END,f"{n}\n")
        number_log.see(tk.END)
        number_log.config(state="disabled")
    except Exception as e:
        log_error(e)

def safe_type_number(n):
    try:
        pyautogui.typewrite(str(n))
        pyautogui.press("enter")
    except Exception as e:
        log_error(e)

def add_number(n):
    try:
        if state["shuffle_numbers"]:
            n=random.randint(state["min_number"],state["max_number"])
        if n not in numbers_db:
            numbers_db.append(n)
            state["typed_count"]+=1
            state["typed_chars"]+=len(str(n))
            typed_counter.set(f"Numbers: {state['typed_count']} | Chars: {state['typed_chars']}")
            number_log_update(n)
            if state["auto_save"]:
                save_db()
            threading.Thread(target=lambda:safe_type_number(n),daemon=True).start()
            train_model()
            update_ai_prediction()
            return True
        return False
    except Exception as e:
        log_error(e)
        return False

def toggle_run():
    state["running"]=not state["running"]
    start_btn.config(text="Stop" if state["running"] else "Start")
    threading.Thread(target=run_loop,daemon=True).start()

def run_loop():
    while state["running"]:
        try:
            n=random.randint(state["min_number"],state["max_number"])
            add_number(n)
            time.sleep(state["delay"])
        except Exception as e:
            log_error(e)

def clear_db():
    if messagebox.askyesno("Confirm","Clear all saved numbers?"):
        numbers_db.clear()
        state["typed_count"]=0
        state["typed_chars"]=0
        typed_counter.set(f"Numbers: {state['typed_count']} | Chars: {state['typed_chars']}")
        save_db()
        number_log_update("Database cleared")

start_btn=create_gradient_button(control_frame,"Start",toggle_run)
clear_btn=create_gradient_button(control_frame,"Clear DB",clear_db)
ai_btn=create_gradient_button(control_frame,"AI Panel",open_ai_panel)
start_btn.grid(row=0,column=0,padx=10,pady=5)
clear_btn.grid(row=0,column=1,padx=10,pady=5)
ai_btn.grid(row=0,column=2,padx=10,pady=5)

tk.Label(content_frames["Settings"],text="Settings",font=("Segoe UI",16,"bold"),fg=THEME["accent"],bg=THEME["bg"]).pack(pady=10)
settings_panel=tk.Frame(content_frames["Settings"],bg=THEME["panel"],pady=10,padx=10)
settings_panel.pack(pady=5,padx=20,fill="x")

tk.Label(settings_panel,text="Min Number:",font=("Segoe UI",12),fg=THEME["text"],bg=THEME["panel"]).grid(row=0,column=0,sticky="w",pady=5)
min_entry=tk.Entry(settings_panel,width=12)
min_entry.grid(row=0,column=1,padx=10,pady=5)
min_entry.insert(0,str(state["min_number"]))
min_entry.bind("<KeyRelease>",lambda e: state.update({"min_number": int(min_entry.get()) if min_entry.get().isdigit() else state["min_number"]}))

tk.Label(settings_panel,text="Max Number:",font=("Segoe UI",12),fg=THEME["text"],bg=THEME["panel"]).grid(row=1,column=0,sticky="w",pady=5)
max_entry=tk.Entry(settings_panel,width=12)
max_entry.grid(row=1,column=1,padx=10,pady=5)
max_entry.insert(0,str(state["max_number"]))
max_entry.bind("<KeyRelease>",lambda e: state.update({"max_number": int(max_entry.get()) if max_entry.get().isdigit() else state["max_number"]}))

tk.Label(settings_panel,text="Typing Speed (s):",font=("Segoe UI",12),fg=THEME["text"],bg=THEME["panel"]).grid(row=2,column=0,sticky="w",pady=5)
delay_scale=tk.Scale(settings_panel,from_=0.1,to=5.0,resolution=0.1,orient="horizontal",bg=THEME["panel"],fg=THEME["text"],troughcolor="#555555",highlightthickness=0,length=300,command=lambda v: state.update({"delay": float(v)}))
delay_scale.set(state["delay"])
delay_scale.grid(row=2,column=1,padx=10,pady=5)

shuffle_var=tk.BooleanVar(value=state["shuffle_numbers"])
tk.Checkbutton(settings_panel,text="Shuffle Numbers",font=("Segoe UI",12),fg=THEME["text"],bg=THEME["panel"],selectcolor=THEME["panel"],variable=shuffle_var,command=lambda: state.update({"shuffle_numbers": shuffle_var.get()})).grid(row=3,column=0,columnspan=2,sticky="w",pady=5)
auto_save_var=tk.BooleanVar(value=state["auto_save"])
tk.Checkbutton(settings_panel,text="Auto Save DB",font=("Segoe UI",12),fg=THEME["text"],bg=THEME["panel"],selectcolor=THEME["panel"],variable=auto_save_var,command=lambda: state.update({"auto_save": auto_save_var.get()})).grid(row=4,column=0,columnspan=2,sticky="w",pady=5)

update_log_frame=tk.Frame(content_frames["Updates"],bg=THEME["bg"])
update_log_frame.pack(fill="both",expand=True)
update_scroll=tk.Scrollbar(update_log_frame)
update_scroll.pack(side="right",fill="y")
update_log=tk.Text(update_log_frame,bg=THEME["glass"],fg=THEME["text"],state="normal",yscrollcommand=update_scroll.set,font=("Consolas",11))
update_log.pack(fill="both",expand=True,padx=10,pady=10)
update_scroll.config(command=update_log.yview)
update_log.insert(tk.END,"App started\n")

show("Numbers")
root.mainloop()

