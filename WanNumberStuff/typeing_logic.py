import random
import time
import threading
import pyautogui
import json
import os

class TyperLogic:
    def __init__(self, json_file="numbers.json"):
        self.json_file = json_file
        if os.path.exists(json_file):
            with open(json_file, "r") as f:
                self.typed_numbers = json.load(f)
        else:
            self.typed_numbers = []
        self.running = False
        self.delay = 1.3
        threading.Thread(target=self._loop, daemon=True).start()

    def save_numbers(self):
        with open(self.json_file, "w") as f:
            json.dump(self.typed_numbers, f)

    def add_number(self, number):
        if number not in self.typed_numbers:
            self.typed_numbers.append(number)
            self.save_numbers()
            return True
        return False

    def clear_numbers(self):
        self.typed_numbers.clear()
        self.save_numbers()

    def toggle(self):
        self.running = not self.running

    def set_delay(self, val):
        self.delay = float(val)

    def _loop(self):
        while True:
            if self.running:
                number = random.randint(100, 500000)
                if self.add_number(number):
                    pyautogui.typewrite(str(number))
                    pyautogui.press("enter")
                time.sleep(self.delay)
            else:
                time.sleep(0.1)
