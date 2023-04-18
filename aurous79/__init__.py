import os
from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    # add configurations here
    return app


app = create_app()


# Flask-Mail config
def init_mail(app: Flask) -> Mail:
    app.config.update(
        {
            "DEBUG": True,
            "MAIL_SERVER": "smtp.gmail.com",
            "MAIL_PORT": 587,
            "MAIL_USE_TLS": True,
            "MAIL_USE_SSL": False,
            "MAIL_USERNAME": os.environ["AUROUS79_EMAIL"],
            "MAIL_PASSWORD": os.environ["AUROUS79_EMAIL_PASSWORD"],
            "MAIL_DEFAULT_SENDER": (
                "Aurous79®",
                os.environ["AUROUS79_EMAIL"],
            ),  # name/title, email
            "MAIL_MAX_EMAILS": 100,
        }
    )
    mail = Mail(app)
    return mail
