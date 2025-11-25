from tkinter import colorchooser

app_bg = "#000000"
app_fg = "#ffffff"
btn_bg = "#ffffff"
btn_fg = "#000000"

def choose_bg_color(root, main_frame, settings_frame, update_widgets):
    color = colorchooser.askcolor(title="Choose Background Color")[1]
    if color:
        global app_bg
        app_bg = color
        root.configure(bg=app_bg)
        main_frame.configure(bg=app_bg)
        settings_frame.configure(bg=app_bg)
        update_widgets()

def choose_fg_color(update_widgets):
    color = colorchooser.askcolor(title="Choose Text Color")[1]
    if color:
        global app_fg
        app_fg = color
        update_widgets()

def choose_btn_bg_color(update_widgets):
    color = colorchooser.askcolor(title="Choose Button Background")[1]
    if color:
        global btn_bg
        btn_bg = color
        update_widgets()

def choose_btn_fg_color(update_widgets):
    color = colorchooser.askcolor(title="Choose Button Text")[1]
    if color:
        global btn_fg
        btn_fg = color
        update_widgets()
