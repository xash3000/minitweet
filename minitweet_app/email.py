from flask.ext.mail import Message

from . import app, mail


def send_email(to, subject, template):
    """
    send email to users
    """
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
