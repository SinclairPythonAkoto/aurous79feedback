from sqlalchemy import Column, String, Integer, DateTime, Text
from aurous79.extension import Base


class FeedbackForm(Base):
    __tablename__ = "aurous_feedback"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(20), nullable=False)
    age = Column("age", Integer, nullable=False)
    sex = Column("sex", String(6), nullable=False)
    first_visit = Column("first_visit", Integer, nullable=False)  # 1 or 0
    return_visit = Column("return_visit", Integer, nullable=False)  # 1 or 0
    clean = Column("cleaniness", Integer, nullable=False)
    service = Column("customer_service", Integer, nullable=False)
    speed = Column("speed", Integer, nullable=False)
    shisha = Column("shisha", Integer, nullable=False)  # 1 or 0
    comment = Column(
        "comment", Text, nullable=True
    )  # the only entry that can be left empty
    email = Column("email", String(50), nullable=False)
    timestamp = Column("timestamp", DateTime, nullable=False)

    def __init__(
        self,
        name,
        age,
        sex,
        first_visit,
        return_visit,
        clean,
        service,
        speed,
        shisha,
        comment,
        email,
        timestamp,
    ):
        self.name = name
        self.age = age
        self.sex = sex
        self.first_visit = first_visit
        self.return_visit = return_visit
        self.clean = clean
        self.service = service
        self.speed = speed
        self.shisha = shisha
        self.comment = comment
        self.email = email
        self.timestamp = timestamp


class EmailLibrary(Base):
    __tablename__ = "email_library"
    id = Column("id", Integer, primary_key=True)
    customer_name = Column("name", String(30))
    customer_email = Column("email", String(50))

    def __init__(self, customer_name, customer_email):
        self.customer_name = customer_name
        self.customer_email = customer_email
