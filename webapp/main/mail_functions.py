from . import mail_manager
import flask_mail

def send_mail(title, body, recipient):
    # Create a message object
    msg = flask_mail.Message(
        subject=title,
        body=body,
        recipients=[recipient],
    )

    # Send it using mail_manager.send
    mail_manager.send(msg)


