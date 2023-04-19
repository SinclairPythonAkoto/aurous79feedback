from aurous79 import app
from aurous79.extension import SessionLocal
from aurous79.models import FeedbackForm


def minimum_age(age: int) -> bool:
    """check if the age is <= 16"""
    if age <= 15:
        return False  # return to home
    else:
        return True  # continue to feedback form


def check_age(age: int) -> bool:
    """Check if age is 16 - 18+ and apply discount accordingly"""
    if age <= 17:
        return False  # 5% discount
    else:
        return True  # 10% discount
