import os

from flask import Flask, render_template, url_for, request, redirect, flash, session
from functools import wraps
from db_table import * 
from graph_func import * 
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
    MAIL_USERNAME = os.getenv("AUROUS_EMAIL"),
    MAIL_PASSWORD = os.getenv("AUROUS_EMAIL_PW"),
    MAIL_DEFAULT_SENDER = ('Aurous 79®', os.getenv("AUROUS_EMAIL")), #('NAME OR TITLE OF SENDER', 'SENDER EMAIL ADDRESS')
    MAIL_MAX_EMAILS = 5
))

mail = Mail(server)

server.secret_key = os.getenv("SECRET_KEY")

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to sign in first')
            return redirect(url_for('login'))
    return wrap


Session = sessionmaker(bind=engine)
db_session = Session()

title = "Aurous79®"

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
        tdate = str(datetime.now().date())
        if email == confirm:
            db_entry = AurousFeedback(name, age, sex, visit, return_v, appearance, customer, serviceSpeed, shisha, comment, email, tdate)
            db_session.add(db_entry)
            db_session.commit()

            msg = Message('My Aurous® Discount!', recipients=[email])
            msg.body = f'Thank you {name} for completing our feedback form! You have earned 5"%" off from your bill.\n\nTo gain your discount please show this email to the cashier.\n\nPlease note that this expires 24hrs after {time}, {tdate}.\n\n\n'

            with server.open_resource('aurouslogo.jpg') as logo:
                msg.attach('aurouslogo.jpg', 'image/jpeg', logo.read())

            mail.send(msg)

            flash(f'Thank you {name} for your feedback!')
            return redirect(url_for('home'))
        else:
            error = "Please provide a correct email to recieve your discount!"
            return render_template('feedback.html', title=title, error=error)

@server.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    admin = request.form.get("username")
    admin_pw = request.form.get("password")
    if request.method == 'GET':
        return render_template('login.html', title=title)
    else:
        if admin == os.getenv("ADMIN_USERNAME") and admin_pw == os.getenv("ADMIN_PW"):
            session['logged_in'] = True
            flash(f'Welcome back to Aurous79!')
            return redirect(url_for('admin'))
        else:
            error = "Invalid username and/or password.  You must be management of Aurous79 to login."
    return render_template('admin.html', error=error, title=title)

@server.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    data = db_session.query(AurousFeedback).all()
    return render_template('admin.html', title=title, data=data)

@server.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('See you soon!')
    return redirect(url_for('home'))

@server.route('/aurousemail', methods=['GET', 'POST'])
@login_required
def aurousemail():
    if request.method == 'GET':
        return render_template('aurousemail.html', title=title)
    else:
        sub = request.form.get("sub")
        content = request.form.get("email_content")
        # if feedback list is picked...
        if request.form.get("massEmail") == 'feedback_lib':
        # else if email library picked...
            db_emails = db_session.query(AurousFeedback.email).all()
            emails = db_emails # this stores all emails in database
            # emails is a list of tuples
            sendEmail = []
            for e in emails: sendEmail += e
            # this is another way of writing a for-loop
            # this looping through every email in emails and putting it into a list
            # this pprocess removes the tuples and leaves emails in list

            msg = Message(f'{sub}', recipients=sendEmail)
            msg.body = f'{content}\n\n'

            with server.open_resource('aurouslogo.jpg') as logo:
                msg.attach('aurouslogo.jpg', 'image/jpeg', logo.read())

            mail.send(msg)
            flash('Your email has been sent!')
            return render_template('aurousemail.html', title=title)
        elif request.form.get("massEmail") == 'email_lib':
            db_emails = db_session.query(EmailLibrary.lib_mail).all()
            emails = db_emails
            sendEmail = []
            for e in emails: sendEmail += e

            msg = Message(f'{sub}', recipients=sendEmail)
            msg.body = f'{content}\n\n'

            with server.open_resource('aurouslogo.jpg') as logo:
                msg.attach('aurouslogo.jpg', 'image/jpeg', logo.read())

            mail.send(msg)
            flash('Your email has been sent!')
            return render_template('aurousemail.html', title=title)
        else:
            if request.form.get("massEmail") == None:
                flash(f'You forgot to select an email source!')
                return redirect(url_for('aurousemail'))

@server.route('/email1', methods=['GET', 'POST'])
@login_required
def email1():
    if request.method == 'GET':
        return render_template('email1.html', title=title)
    else:
        email = request.form.get("name")
        sub = request.form.get("sub")
        content = request.form.get("email_content")

        msg = Message(f'{sub}', recipients=[email])
        msg.body = f'{content}\n\n'

        with server.open_resource('aurouslogo.jpg') as logo:
            msg.attach('aurouslogo.jpg', 'image/jpeg', logo.read())

        mail.send(msg)
        flash(f'Your email has been sent to {email}!')
        return render_template('email1.html', title=title)

@server.route('/emaillib', methods=['GET', 'POST'])
@login_required
def emaillib():
    if request.method == 'GET':
        return render_template('emaillib.html', title=title)
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        db_entry = EmailLibrary(name, email)
        db_session.add(db_entry)
        db_session.commit()
        data = db_session.query(EmailLibrary).order_by(EmailLibrary.id).all()
        flash(f'You have stored {name}\'s email to the Aurous79® Email Library!' )
        return render_template('emaillib.html', title=title, data=data)


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

# creating your graphs
app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/'
)

app.layout = html.Div(children=[
    html.H1(children='Aurous79 Customer Analysis'),

    html.Div(children='''
        Aurous79 Customer Analysis
    '''),

    dcc.Graph(
        id='aurous-graph1',
        figure={
            'data': [
                {'x': [1], 'y': [y_men()], 'type': 'bar', 'name': 'Males'},
                {'x': [2], 'y': [y_women()], 'type': 'bar', 'name': 'Females'},
            ],
            'layout': {
                'title': 'Aurous79® Visitors by Gender'
            },
        },

    ),
    html.Div('''
        This graph displays the contast bewteen male & female customers who complete the Aurous79 feedback form.
    '''),
    dcc.Graph(
        id='aurous-graph2',
        figure={
            'data': [
                {'x': [1], 'y': [y_visitors()], 'type': 'bar', 'name': 'New Visitors'},
                {'x': [2], 'y': [y_comeback()], 'type': 'bar', 'name': 'Customer Service'},
                {'x': [3], 'y': [y_shisha()], 'type': 'bar', 'name': 'Tried Shisha'},
            ],
            'layout': {
                'title': 'Aurous79® Customer Relations'
            },
        },

    ),
    html.Div('''
        This graph displays the number of customers that were first time customers, customers that would return and customers that tried the shisha.
    '''),
    dcc.Graph(
        id='aurous-graph3',
        figure={
            'data': [
                {'x': [x_clean()], 'y': [y_clean()], 'type': 'bar', 'name': 'Cleanliness Rating'},
                {'x': [x_service()], 'y': [y_service()], 'type': 'bar', 'name': 'Customer Service Rating'},
                {'x': [x_speed()], 'y': [y_speed()], 'type': 'bar', 'name': 'Speed Rating'},
            ],
            'layout': {
                'title': 'Overall Aurous79® Customer Rating'
            },
        },

    ),
    html.Div('''
        This graph displays the average ranking (out of 5) for Cleanliness, Customer Service and Speed by customers.  The total amount of customers are displayed on the X axis below.
    '''),
])


if __name__ == '__main__':
    app.run_server(debug=True)