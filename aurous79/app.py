import os
from aurous79 import app  # import Flask app from init file
from typing import List, Dict
from flask import render_template, url_for, request, redirect, flash, session
from functools import wraps
from aurous79.extension import init_db, SessionLocal
from aurous79.models import FeedbackForm, EmailLibrary
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
        return render_template("home.html", feedback=feedback ,title=title)

@app.route("/feedback")
def feedback():
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
