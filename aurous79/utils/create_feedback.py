from aurous79 import app
from aurous79.extension import SessionLocal
from aurous79.models import FeedbackForm
from datetime import datetime


def create_feedback(
    name: str,
    age: int,
    sex: str,
    first_visit: str,
    return_visit: str,
    clean: int,
    service: int,
    speed: int,
    food_quality: int,
    shisha: str,
    comment: str,
    email: str,
) -> FeedbackForm:
    """Create a new feedback form"""
    with app.app_context():
        session: SessionLocal = SessionLocal()
        new_feedback: FeedbackForm = FeedbackForm(
            name=name,
            age=age,
            sex=sex,
            first_visit=first_visit,
            return_visit=return_visit,
            clean=clean,
            service=service,
            speed=speed,
            food_quality=food_quality,
            shisha=shisha,
            comment=comment,
            email=email.lower(),
            timestamp=datetime.now(),
        )
        session.add(new_feedback)
        session.commit()
    return new_feedback
