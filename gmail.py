import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

def email_alert(subject, body, to):

    msg = EmailMessage()
    msg.set_content(body)

    gmail_user = 'ravnshoej.gaming@gmail.com'
    gmail_password = os.getenv("GMAIL_PASSWORD")
    msg['Subject'] = subject
    msg['From'] = os.getenv("GMAIL_EMAIL")
    msg['To'] = to

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(gmail_user, gmail_password)
    s.send_message(msg)
    s.quit()

if __name__ == '__mail__':
    email_alert("Server er nede","Serveren er nede","tron.999@hotmail.com")