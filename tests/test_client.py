import smtplib
from email.message import EmailMessage


message = EmailMessage()
message["From"] = "sender@example.com"
message["To"] = "receiver@example.com"
message["Subject"] = "My first MailBridge email"

message.set_content(
    "Hello from MailBridge!\n"
    "This is my first complete email."
)


with smtplib.SMTP("127.0.0.1", 2525) as client:
    client.set_debuglevel(1)

    client.send_message(message)