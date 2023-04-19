from aurous79 import app
from aurous79.extension import SessionLocal
from aurous79.models import FeedbackForm


def validate_email(email: str, confirmation: str) -> bool:
    """Validate an email address by checking if the email is valid
    and if the email matches the confirmation email.
    """
    if email == confirmation:
        return True
    else:
        return False


def find_email(email: str) -> bool:
    """Check if the email already exists in the database"""
    with app.app_context():
        session: SessionLocal = SessionLocal()
        email_exists: bool = session.query(FeedbackForm).filter_by(email=email).first()
        if email_exists is None:
            return False  # 10% discount
        else:
            return True  # 5% discount
