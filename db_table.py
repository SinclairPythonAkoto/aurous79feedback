import os

from sqlalchemy.orm import sessionmaker, relationship

# # this part is needed to create session to query database.  this should be JUST BELOW app.config..
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select
meta = MetaData()
engine = create_engine(os.getenv("DATABASE_URL"), echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from datetime import datetime
# this is added to create a date stamp for SQL
# done in such a way that the data is stored in a String format
# instead of using Date data-type

# database here
class AurousFeedback(Base):
    __tablename__ = 'aurous_feedback'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(20))
    age = Column('age', Integer)
    sex = Column('sex', String(6))
    f_visit = Column('first_visit', String(3))
    comeback = Column('return_visit', String(3))
    clean = Column('cleanliness', Integer)
    service = Column('customer_service', Integer)
    speed = Column('speed', Integer)
    shisha = Column('shisha', String(3))
    comment =  Column('comment', String(480))
    email = Column('email', String(40))
    dateStamp = Column('date_stamp', String(), nullable=False, default = datetime.now().today())
    
    def __init__(self, name, age, sex, f_visit, comeback, clean, service, speed, shisha, comment, email, datetime):
        self.name = name
        self.age = age
        self.sex = sex
        self.f_visit = f_visit
        self.comeback = comeback
        self.clean = clean
        self.service = service
        self.speed = speed
        self.shisha = shisha
        self.comment = comment
        self.email = email
        self.datetime = datetime


class EmailLibrary(Base):
    __tablename__ = 'email_library'
    id = Column('id', Integer, primary_key=True)
    lib_name = Column('name', String(30))
    lib_mail = Column('email', String(50))

    def __init__(self, lib_name, lib_mail):
        self.lib_name = lib_name
        self.lib_mail = lib_mail