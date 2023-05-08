import sys
import time
import pyautogui
import tkinter as tk

macro = [] # Define macro as a global variable
recording = False

# Define function for start recording button
def start_record():
    global recording
    global macro
    recording = True
    macro = []  # clear the macro list
    print("Recording started")

# Define function for stop recording button
def stop_record():
    global recording
    recording = False
    print("Recording stopped")
    print(macro)  # print the macro list to see if it contains any data

# Define function to be called when mouse is moved
def on_move(x, y):
    if recording:
        print("Mouse moved to ({0}, {1})".format(x, y))
        macro.append(('move', x, y, time.time()))  # add move action to macro list

# Define function to be called when mouse is clicked
def on_click(x, y, button, pressed):
    if recording and pressed:
        print("Mouse clicked at ({0}, {1}) with {2} button".format(x, y, button))
        macro.append(('click', button, x, y, time.time()))  # add click action to macro list

# Define function for play macro button
def play_macro():
    print("Playing macro")
    try:
        with open('macro.txt', 'r') as f:
            for line in f:
                line = line.strip()
                actions = line.split(',')
                action_type = actions[0]
                if action_type == 'move':
                    x = int(actions[1])
                    y = int(actions[2])
                    duration = float(actions[3])
                    pyautogui.moveTo(x, y, duration=duration)
                elif action_type == 'click':
                    button = actions[1]
                    x = int(actions[2])
                    y = int(actions[3])
                    duration = float(actions[4])
                    pyautogui.moveTo(x, y, duration=duration)
                    pyautogui.click(button=button, duration=duration)
                elif action_type == 'keypress':
                    key = actions[1]
                    duration = float(actions[2])
                    pyautogui.press(key, duration=duration)
    except FileNotFoundError:
        print("Macro file not found. Please record a macro first.")


# Define function for export macro button
def export_macro():
    print("Exporting macro")
    if macro:
        with open('macro.txt', 'w') as f:
            for action in macro:
                f.write(','.join(str(x) for x in action) + '\n')
    else:
        print("Macro is empty")

# Define function for import macro button
def import_macro():
    global macro
    macro = []
    print("Importing macro")
    with open('macro.txt', 'r') as f:
        for line in f:
            line = line.strip()
            actions = line.split(',')
            macro.append(actions)
# GUI

# Create GUI window
window = tk.Tk()
window.title("Macro Recorder")

# Create buttons
record_button = tk.Button(window, text="Record", command=start_record)
play_button = tk.Button(window, text="Play", command=play_macro)
stop_button = tk.Button(window, text="Stop", command=stop_record)
export_button = tk.Button(window, text="Export Macro", command=export_macro)
import_button = tk.Button(window, text="Import Macro", command=import_macro)

# Add buttons to window
record_button.pack()
play_button.pack()
stop_button.pack()
export_button.pack()
import_button.pack()

# Start GUI loop
window.mainloop()
