from . import mail_manager
import flask_mail

def send_mail(title, body, recipients):

    if type(recipients) == str:
        recipients = [recipients]

    # Create a message object
    msg = flask_mail.Message(
        subject=title,
        body=body,
        recipients=recipients,
    )

    # Send it using mail_manager.send
    mail_manager.send(msg)


