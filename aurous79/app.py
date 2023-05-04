import os
from aurous79 import app, init_mail
from typing import List, Dict
from flask import render_template, url_for, request, redirect, flash, session
from functools import wraps
from datetime import datetime
from flask_mail import Message
from time import strftime
from aurous79.extension import init_db, SessionLocal
from aurous79.models import FeedbackForm, EmailLibrary
from aurous79.utils.validate_email import validate_email, find_email
from aurous79.utils.create_feedback import create_feedback
from aurous79.utils.validate_age import minimum_age, check_age
from aurous79.utils.create_email import send_email
# from aurous79.utils.login_required import login_required
from dotenv import load_dotenv

load_dotenv()

init_db()


# config your db
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["AUROUS79_DB"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

title = os.environ["AUROUS79_TITLE"]

# secret key for session
app.secret_key = os.environ["AUROUS79_SECRET_KEY"]


from functools import wraps
from flask import session, redirect, url_for

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is None:
            flash('You need to log in first')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function



@app.route("/")
def home():
    session: SessionLocal = SessionLocal()
    feedback: List[FeedbackForm] = session.query(FeedbackForm).first()
    if feedback is None:
        message: str = "The feedback board is empty."
        return render_template("home.html", message=message, title=title)
    else:
        feedback: List[FeedbackForm] = session.query(FeedbackForm).all()
        return render_template("home.html", feedback=feedback, title=title)


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "GET":
        return render_template("feedback.html", title=title)
    name = request.form["name"]
    age = request.form["age"]
    sex = request.form["sex"]
    first_visit = request.form["first_visit"]
    return_visit = request.form["return_visit"]
    cleanliness = request.form["cleanliness"]
    customer_service = request.form["customer_service"]
    service_speed = request.form["speed"]
    food_quality = request.form["food_quality"]
    shisha = request.form["shisha"]
    customer_comment = request.form["customer_comment"]
    customer_email = request.form["customer_email"]
    confirm_email = request.form["confirm_email"]

    # check if customer is < 16
    verified_age: bool = minimum_age(int(age))
    if verified_age is False:
        message = "You must be 16 or older to complete this form."
        return render_template("home.html", message=message, title=title), 308
    else:
        # check if customer is >= 18
        over_18: bool = check_age(int(age))
        if over_18 is True:
            # check if email already exists in db
            email_exists: bool = find_email(customer_email)
            if email_exists is True:
                # add feedback to db with 5% email
                new_feedback: FeedbackForm = create_feedback(
                    name,
                    int(age),
                    sex,
                    first_visit,
                    return_visit,
                    int(cleanliness),
                    int(customer_service),
                    int(service_speed),
                    int(food_quality),
                    shisha,
                    customer_comment,
                    customer_email,
                )
                discount: str = "5%"
                send_customer_email: Message = send_email(
                    name, customer_email, discount
                )
                flash(f"Thank you {name} for your feedback!")
                return redirect(url_for("home")), 201
            else:
                # if email does not exist, add feedback to db with 10% email
                validate_customer_email: bool = validate_email(
                    customer_email, confirm_email
                )
                if validate_customer_email is True:
                    new_feedback: FeedbackForm = create_feedback(
                        name,
                        int(age),
                        sex,
                        first_visit,
                        return_visit,
                        int(cleanliness),
                        int(customer_service),
                        int(service_speed),
                        int(food_quality),
                        shisha,
                        customer_comment,
                        customer_email,
                    )
                    discount: str = "10%"
                    send_customer_email: Message = send_email(
                        name, customer_email, discount
                    )
                    flash(f"Thank you {name} for your feedback!")
                    return redirect(url_for("home")), 201
                # if invalid emails, return error message
                error_message: str = "The email you entered does not match. Please try again to recieve your discount."
                return (
                    render_template(
                        "feedback.html", error_message=error_message, title=title
                    ),
                    400,
                )
        else:
            # if customer is under 18, send 5% email
            validate_customer_email: bool = validate_email(
                customer_email, confirm_email
            )
            if validate_customer_email is True:
                new_feedback: FeedbackForm = create_feedback(
                    name,
                    int(age),
                    sex,
                    first_visit,
                    return_visit,
                    int(cleanliness),
                    int(customer_service),
                    int(service_speed),
                    int(food_quality),
                    shisha,
                    customer_comment,
                    customer_email,
                )
                discount = "5%"
                send_customer_email: Message = send_email(
                    name, customer_email, discount
                )
                flash(f"Thank you {name} for your feedback!")
                return redirect(url_for("home")), 201
            # if invalid emails, return error message
            error_message: str = "The email you entered does not match. Please try again to recieve your discount."
            return (
                render_template(
                    "feedback.html", error_message=error_message, title=title
                ),
                400,
            )


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        admin = request.form["username"]
        admin_password = request.form["password"]
        if admin == os.getenv("ADMIN_USERNAME") and admin_password == os.getenv("ADMIN_PASSWORD"):
            session['logged_in'] = True
            flash("Welcome back to Aurous79!")
            return redirect(url_for("admin"))
        else:
            error = "Invalid username and/or password. You must be management of Aurous79 to login."
    return render_template("login.html", error=error)



@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")


@app.route("/logout")
def logout():
    return redirect(url_for("home"))


@app.route("/report")
def report():
    return render_template("report.html")


@app.route("/send-email")
def send_single_email():
    return render_template("send_email.html")


@app.route("/mass-emails")
def send_mass_emails():
    return render_template("mass_emails.html")


@app.route("/email-library")
def email_library():
    return render_template("email_library.html")


if __name__ == "__main__":
    app.run(debug=True)


# status codes
# 200 - ok
# 201 - created
# 202 - accepted
# 204 - no content
# 301 - moved permanently
# 302 - found
# 304 - not modified
# 307 - temporary redirect (same as 302)
# 308 - permanent redirect (same as 301)

# 400 - bad request
# 401 - unauthorized
# 403 - forbidden
# 404 - not found
# 405 - method not allowed
# 500 - internal server error
# 501 - not implemented
