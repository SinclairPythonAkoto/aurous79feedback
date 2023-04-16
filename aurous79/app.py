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


@app.route("/")
def index():
    return "hello world"


if __name__ == "__main__":
    app.run(debug=True)
