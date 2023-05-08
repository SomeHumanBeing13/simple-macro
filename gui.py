import tkinter as tk
from macro_function import start_record, stop_record, play_macro, export_macro, macro_list

# Create GUI window
window = tk.Tk()
window.title("Macro Recorder")

# Create buttons
record_button = tk.Button(window, text="Record", command=start_record)
play_button = tk.Button(window, text="Play", command=play_macro)
stop_button = tk.Button(window, text="Stop", command=stop_record)
export_button = tk.Button(window, text="Export Macro", command=lambda: export_macro(macro_list))
# import_button = tk.Button(window, text="Import Macro", command=import_macro)

# Add buttons to window
record_button.pack()
play_button.pack()
stop_button.pack()
export_button.pack()
# import_button.pack()

# Start GUI loop
window.mainloop()
