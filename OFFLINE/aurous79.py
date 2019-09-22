from flask import Flask, render_template, url_for, request, redirect, flash, session
from functools import wraps
from flask_mail import Mail, Message
import dash
import dash_core_components as dcc
import dash_html_components as html

server = Flask(__name__)

# Flask-Mail config
server.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'sinclair.python@gmail.com',
    MAIL_PASSWORD = 'Shalieka2017',
    MAIL_DEFAULT_SENDER = ('Aurous 79®', 'sinclair.python@gmail.com'), #('NAME OR TITLE OF SENDER', 'SENDER EMAIL ADDRESS')
    MAIL_MAX_EMAILS = 5
))

mail = Mail(server)

server.secret_key = "habibi"

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to sign in first')
			return redirect(url_for('login'))
	return wrap

from sqlalchemy.orm import sessionmaker, relationship

# # this part is needed to create session to query database.  this should be JUST BELOW app.config..
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select
meta = MetaData()
engine = create_engine("postgresql://postgres:161086@localhost/test-db-02", echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

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
    confirm = Column('confirm_email', String(40))
    timeStamp = Column('time_stamp', String(5))
    dateStamp = Column('date_stamp', String())
    
    def __init__(self, name, age, sex, f_visit, comeback, clean, service, speed, shisha, comment, email, confirm, timeStamp, datetime):
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
        self.confirm = confirm
        self.timeStamp = timeStamp
        self.datetime = datetime

Session = sessionmaker(bind=engine)
db_session = Session()

title = "Aurous79"

@server.route('/')
def home():
	data = db_session.query(AurousFeedback).order_by(AurousFeedback.id).all()
	return render_template('home.html', title=title, data=data)

@server.route('/feedback', methods=['GET', 'POST'])
def feedback():
	if request.method == 'GET':
		return render_template('feedback.html', title=title)
	else:
		from time import strftime
		from datetime import datetime
		name = request.form.get("name")
		age = request.form.get("age")
		sex = request.form.get("sex")
		visit = request.form.get("firstVisit")
		return_v = request.form.get("return_v")
		appearance = request.form.get("cleanliness")
		customer = request.form.get("customerService")
		serviceSpeed = request.form.get("speed")
		shisha = request.form.get("shisha")
		comment = request.form.get("comment")
		email = request.form.get("email")
		confirm = request.form.get("confirmEmail")
		time = str(datetime.now().time())
		tdate = datetime.now().date()
		if email == confirm:
			db_entry = AurousFeedback(name, age, sex, visit, return_v, appearance, customer, serviceSpeed, shisha, comment, email, confirm, time, tdate)
			db_session.add(db_entry)
			db_session.commit()

			msg = Message('My Aurous® Discount!', recipients=[email])
			msg.body = f'Thank you {name} for completing our feedback form! You have earned 5"%" off from your bill.\n\nTo gain your discount please show this email to the cashier.\n\nPlease note that this expires 24hrs after {tdate} {time}.\n\n\n'

			with app.open_resource('aurouslogo.jpg') as logo:
				msg.attach('aurouslogo.jpg', 'image/jpeg', logo.read())



			flash(f'Thank you {name} for your feedback!')
			return redirect(url_for('home'))
		else:
			error = "Please provide a correct email to send the discount to!"
			return render_template('feedback.html', title=title, error=error)

@server.route('/login', methods=['GET', 'POST'])
def login():
	title = "Aurous79 Login"
	error = None
	admin = request.form.get("username")
	admin_pw = request.form.get("password")
	if request.method == 'GET':
		return render_template('login.html', title=title)
	else:
		if admin == "admin" and admin_pw == "admin":
			session['logged_in'] = True
			flash(f'Welcome back to Aurous79!')
			return redirect(url_for('admin'))
		else:
			error = "Invalid username and/or password.  You must be management of Aurous79 to login."
	return render_template('admin.html', error=error, title=title)

@server.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
	title = "Aurous79 Admin"
	data = db_session.query(AurousFeedback).all()
	return render_template('admin.html', title=title, data=data)

@server.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('See you soon!')
	return redirect(url_for('home'))

@server.route('/report', methods=['GET', 'POST'])
@login_required
def report():
	title = "Aurous79 Reports"
	a_rpt = request.form.get("run_rpt")
	if request.method == 'GET':
		return render_template('report.html', title=title)
	else:
		if a_rpt == 'male':
			db_entry = db_session.query(AurousFeedback).filter(AurousFeedback.sex=='male')
			male_rpt = db_entry.all()
			return render_template('report.html', title=title, male_rpt=male_rpt)
		elif a_rpt == 'female':
			db_entry = db_session.query(AurousFeedback).filter(AurousFeedback.sex=='female')
			female_rpt = db_entry.all()
			return render_template('report.html', title=title, female_rpt=female_rpt)
		elif a_rpt == 'n_visit':
			db_entry = db_session.query(AurousFeedback).filter(AurousFeedback.f_visit=='yes')
			new_visit_rpt = db_entry.all()
			return render_template('report.html', title=title, new_visit_rpt=new_visit_rpt)
		elif a_rpt == 'r_visit':
			db_entry = db_session.query(AurousFeedback).filter(AurousFeedback.comeback=='yes')
			return_visit_rpt = db_entry.all()
			return render_template('report.html', title=title, return_visit_rpt=return_visit_rpt)
		elif a_rpt == 'shisha':
			db_entry = db_session.query(AurousFeedback).filter(AurousFeedback.shisha=='yes')
			shisha_rpt = db_entry.all()
			return render_template('report.html', title=title, shisha_rpt=shisha_rpt)
		elif a_rpt == 'clean':
			data = db_session.query(AurousFeedback).order_by(AurousFeedback.id).all()
			clean_rpt = data
			return render_template('report.html', title=title, clean_rpt=clean_rpt)
		elif a_rpt == 'service':
			data = db_session.query(AurousFeedback).order_by(AurousFeedback.id).all()
			service_rpt = data
			return render_template('report.html', title=title, service_rpt=service_rpt)
		elif a_rpt == 'speed':
			data = db_session.query(AurousFeedback).order_by(AurousFeedback.id).all()
			speed_rpt = data
			return render_template('report.html', title=title, speed_rpt=speed_rpt)
		else:
			if a_rpt == None:
				flash('You need to select a reprot to run!')
				return redirect(url_for('report'))



if __name__ == '__main__':
    server.run(debug=True)