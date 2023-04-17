import os
from aurous79 import app  # import Flask app from init file
from typing import List, Dict
from flask import render_template, url_for, request, redirect, flash, session
from functools import wraps
from datetime import datetime
from time import strftime
from aurous79.extension import init_db, SessionLocal
from aurous79.models import FeedbackForm, EmailLibrary
from aurous79.utils.validate_email import validate_email
from dotenv import load_dotenv

load_dotenv()

init_db()

# create your db
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["AUROUS79_DB"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

title = os.environ["AUROUS79_TITLE"]


@app.route("/")
def home():
    session: SessionLocal = SessionLocal()
    feedback: List[FeedbackForm] = session.query(FeedbackForm).first()
    if feedback is None:
        message: str = "The feedback board is empty."
        return render_template("home.html", message=message, title=title)
    else:
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
    comment = request.form["comment"]
    customer_email = request.form["customer_email"]
    confirm_email = request.form["confirm_email"]
    feedback_date = datetime.now()

    # add to db if email is valid
    validate_customer_email: bool = validate_email(customer_email, confirm_email)
    if validate_customer_email is True:
        # print("Email is valid")
        session: SessionLocal = SessionLocal()
        new_feedback: FeedbackForm = FeedbackForm(name, age, sex, first_visit, return_visit, cleanliness, customer_service, service_speed, food_quality, shisha, comment, customer_email, feedback_date)
        session.add(new_feedback)
        session.commit()

        # send email to customer
    else:
        error_message = (
            "Emails do not match. Please try again to recieve your discount."
        )
        print(error_message)
        return (
            render_template("feedback.html", error_message=error_message, title=title),
            400,
        )
    return render_template("feedback.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/login")
def login():
    return render_template("login.html")


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

# 400 - bad request
# 401 - unauthorized
# 403 - forbidden
# 404 - not found
# 405 - method not allowed
# 500 - internal server error
# 501 - not implemented
