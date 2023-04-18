from aurous79 import app, init_mail
from flask_mail import Message
from datetime import datetime

mail = init_mail(app)

email_timestamp = datetime.now().strftime("%H:%M")
email_datestamp = datetime.now().strftime("%d/%m/%Y")


def create_5P_discount_email(name: str, email: str) -> Message:
    """Create an email with a 5% discount"""
    # set up email message
    email_message = Message("My Aurous79® 5% Discount!", recipients=[email])
    email_message.body = (
        f"Thank you {name} for completing our feedback form! You have earned 5%"
        " off from your bill.\n\nTo gain your discount please show this email to the cashier."
        f"\n\nPlease note that this expires 24hrs after {email_timestamp}, {email_datestamp}.\n\n\n"
    )

    # attach image to email
    with app.open_resource("aurouslogo.jpg") as logo:
        email_message.attach("aurouslogo.jpg", "image/jpeg", logo.read())

    # send email
    mail.send(email_message)


def create_10P_discount_email(name: str, email: str) -> Message:
    """Create an email with a 10% discount"""
    # set up email message
    email_message = Message("My Aurous79® 10% Discount!", recipients=[email])
    email_message.body = (
        f"Thank you {name} for completing our feedback form! You have earned 10%"
        " off from your bill.\n\nTo gain your discount please show this email to the cashier."
        f"\n\nPlease note that this expires 24hrs after {email_timestamp}, {email_datestamp}.\n\n\n"
    )

    # attach image to email
    with app.open_resource("aurouslogo.jpg") as logo:
        email_message.attach("aurouslogo.jpg", "image/jpeg", logo.read())

    # send email
    mail.send(email_message)
