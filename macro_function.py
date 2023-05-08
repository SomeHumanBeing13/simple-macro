import time
import json
import pyautogui
import pickle
from tkinter import filedialog

macro = []  # Define macro as a global variable

# Define function for start recording button
def start_record():
    global recording
    recording = True
    global macro
    macro = []  # clear the macro list
    print("Recording started")

# Define function for stop recording button
def stop_record():
    global recording
    recording = False
    print("Recording stopped")
    print(macro)  # print the macro list to see if it contains any data
    return macro

# Define function for on_move
def on_move(x, y):
    global recording
    if recording:
        print("Mouse moved to ({0}, {1})".format(x, y))
        macro.append(('move', x, y, time.time()))

# Define function for on_click
def on_click(x, y, button, pressed):
    global recording
    if recording:
        action = 'click' if pressed else 'release'
        print("{0} at ({1}, {2})".format(action, x, y))
        macro.append(('click', button, x, y, time.time()))

# Define function for on_scroll
def on_scroll(x, y, dx, dy):
    global recording
    if recording:
        if dy > 0:
            direction = 'up'
        else:
            direction = 'down'
        print("Mouse scrolled {0} at ({1}, {2})".format(direction, x, y))
        macro.append(('scroll', direction, x, y, time.time()))

# Define function for on_press
def on_press(key):
    global recording
    if recording:
        try:
            key_name = key.char
        except AttributeError:
            key_name = key.name
        print("Key {0} pressed".format(key_name))
        macro.append(('keypress', key_name, time.time()))

# Define function for on_release
def on_release(key):
    global recording
    if recording:
        try:
            key_name = key.char
        except AttributeError:
            key_name = key.name
        print("Key {0} released".format(key_name))
        macro.append(('keyrelease', key_name, time.time()))

        # play the macro
def play_macro():
    for event in macro:
        if event[0] == 'move':
            pyautogui.moveTo(event[1], event[2])
        elif event[0] == 'click':
            if event[1] == 'left':
                pyautogui.click(event[2], event[3])
            elif event[1] == 'right':
                pyautogui.rightClick(event[2], event[3])
            elif event[1] == 'middle':
                pyautogui.middleClick(event[2], event[3])
        elif event[0] == 'scroll':
            if event[1] == 'up':
                pyautogui.scroll(1)
            elif event[1] == 'down':
                pyautogui.scroll(-1)
        elif event[0] == 'keypress':
            pyautogui.press(event[1])
        elif event[0] == 'keyrelease':
            pyautogui.keyUp(event[1])

            # export the macro
def export_macro(macro_list):
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    with open(filename, "w") as f:
        for action in macro_list:
            f.write(action + "\n")
