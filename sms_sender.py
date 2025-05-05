import smtplib
import datetime
from email.message import EmailMessage
from sms_config import SENDER_EMAIL, GATEWAY_ADDRESS, APP_KEY

class SMSSender():
    def __init__(self, name="Default"):
        self.name = name

    def send_message(self, message):
        msg = EmailMessage()
        msg['From'] = SENDER_EMAIL
        msg['To'] = GATEWAY_ADDRESS
        msg['Subject'] = self.name
        now = datetime.datetime.now().strftime("%c")
        msg.set_content(f"{now}\n\n{message}")

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(SENDER_EMAIL, APP_KEY)
                server.send_message(msg)
            print("SMS sent")
        except Exception as e:
            print(f"Failed to send SMS: {e}")