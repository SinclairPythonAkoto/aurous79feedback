# Aurous79 Feedback Form

This is a simple feedback form for a restuarant called Auraous79 back in 2019.

Using Flask, this feedback form is intended for customers to complete in order to
sign up to the restuarants promotions and giveaways.  Each customer recieves an 
email with a 10% discount for their next visit.  The web app also allows the 
restuarant management to log into the admin and send promos and persnalised ads
directly to the customers (either on mass or individually).

## Installation
Installation requirements:
```
pip install Flask Flask-Mail dash SQLAlchemy datetime python-dotenv black
```

Install app from the command line:
```
pip install -e .
```

Run the Flask app:
```
python3 aurous79/app.py
```

# Formatting
I am using **Python Black** to make sure PEP8 coding standards are enforced.
Python Black can be used to format a single file or multiple file from a directory.
```
# format a single file
black aurous79/extension.py

# format multiple files in a directory
black aurous79/
```