from . import mail_manager
import flask_mail

def send_mail(sender, title, body, recipient):
    # Create a message object
    msg = flask_mail.Message(
        subject=title,
        body=body,
        sender=sender,
        recipients=[recipient],
    )


