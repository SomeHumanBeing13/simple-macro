import time
import json
import pyautogui
import pickle
from tkinter import filedialog
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller

macro = []  # Define macro as a global variable
recording = False
# Define function for start recording button
def start_record():
    global recording
    recording = True
    global macro
    macro = []  # clear the macro list
    print("Recording started")
    print("Recording status: " + str(recording))
    mouse_listener = mouse.Listener( on_click=on_click, on_scroll=on_scroll)
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener.start()
    keyboard_listener.start()

# Define function for stop recording button
def stop_record():
    global recording
    recording = False
    if len(macro) == 0:
     print("WARNING: The macro didn't record anything. It may or may not have failed to record properly.")
    else:
     print("Successfully Recorded the macro!")
    print("Recording status: " + str(recording))
    print(macro)
    return macro



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
        # Remove the corresponding keypress event from macro
        for i in range(len(macro)-1, -1, -1):
            if macro[i][0] == 'keypress' and macro[i][1] == key_name:
                macro.pop(i)
                break


        # play the macro
def play_macro():
    mouse_controller = Controller()
    keyboard_controller = keyboard.Controller()
    for action in macro:
        if action[0] == "click":
            button = action[1]
            x, y = action[2], action[3]
            mouse_controller.position = (x, y)
            time.sleep(0.5)
            try:
                if button == Button.left:
                    mouse_controller.press(Button.left)
                    mouse_controller.release(Button.left)
                elif button == Button.right:
                    mouse_controller.press(Button.right)
                    mouse_controller.release(Button.right)
                else:
                    raise ValueError(f"Invalid button: {button}")
            except Exception as e:
                print(f"Error: {e}")
        elif action[0] == "scroll":
            direction = action[1]
            x, y = action[2], action[3]
            distance = action[4]
            mouse_controller.position = (x, y)
            time.sleep(0.5)
            try:
                if direction == "up":
                    mouse_controller.scroll(0, distance)
                elif direction == "down":
                    mouse_controller.scroll(0, -distance)
                else:
                    raise ValueError(f"Invalid direction: {direction}")
            except Exception as e:
                print(f"Error: {e}")
        elif action[0] == "keypress":
            key = action[1]
            try:
                keyboard_controller.press(key)
                time.sleep(0.5)
                keyboard_controller.release(key)
            except Exception as e:
                print(f"Error: {e}")






            # export the macro
def export_macro(macro):
    with open("macro.json", "w") as f:
        actions = []
        for action in macro:
            if action[0] == "click":
                actions.append({
                    "type": "click",
                    "button": action[1],
                    "x": action[2],
                    "y": action[3]
                })
            elif action[0] == "scroll":
                actions.append({
                    "type": "scroll",
                    "direction": action[1],
                    "x": action[2],
                    "y": action[3],
                    "distance": action[4]
                })
            elif action[0] == "keypress":
                actions.append({
                    "type": "keypress",
                    "key": action[1]
                })
        json.dump(actions, f)
