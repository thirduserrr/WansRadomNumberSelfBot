import random
import time
import threading
import pyautogui
import json
import os

numbers_file = "numbers.json"

if os.path.exists(numbers_file):
    with open(numbers_file, "r") as f:
        typed_numbers = json.load(f)
else:
    typed_numbers = []

running = False
delay = 1.3

def save_numbers():
    with open(numbers_file, "w") as f:
        json.dump(typed_numbers, f)

def add_number(number):
    if number not in typed_numbers:
        typed_numbers.append(number)
        save_numbers()
        return True
    return False

def clear_numbers():
    typed_numbers.clear()
    save_numbers()

def typer_loop():
    global running
    while True:
        if running:
            number = random.randint(100, 500000)
            if add_number(number):
                pyautogui.typewrite(str(number))
                pyautogui.press("enter")
            time.sleep(delay)
        else:
            time.sleep(0.1)
