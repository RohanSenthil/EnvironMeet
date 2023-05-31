from flask_mail import Message

from app import mail

def send_message(recipient, subject, html, body=None):
    new_message = Message(subject, [recipient], body, html)
    mail.send(new_message)
