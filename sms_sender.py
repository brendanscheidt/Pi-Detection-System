import smtplib
import datetime
from email.message import EmailMessage
from sms_config import SENDER_EMAIL, GATEWAY_ADDRESS, APP_KEY

class SMSSender():
    def __init__(self, name="Default"):
        self.name = name
        self.msg = EmailMessage()
        self.msg['From'] = SENDER_EMAIL
        self.msg['To'] = GATEWAY_ADDRESS
        self.msg['Subject'] = self.name
        self.server = smtplib.SMTP('smtp.gmail.com', 587)

    def send_message(self, message):
        date = datetime.datetime.now().strftime("%c")
        self.msg.set_content("\n" + date + "\n" + message)
        self.server.starttls()
        self.server.login(SENDER_EMAIL, APP_KEY)
        self.server.send_message(self.msg)
        self.server.quit()