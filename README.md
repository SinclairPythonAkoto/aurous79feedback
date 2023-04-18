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
pip install Flask flask_mail dash SQLAlchemy datetime python-dotenv black
```

Install app from the command line:
```
pip install -e .
```

Run the Flask app:
```
flask --app aurous79/app.py run
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

# Setting up Flask-Mail
The implementation has changed since the last time I used this library 4x years ago.
Before we just needed to add our Gmail email and password to the app and then turn
on the less secure app option in your Gmail Account.  Now the process is slightly different
becuase the secure app option no longer exists.  Because I have the 2-step verification 
on my Gmail account, I need to naviagate to **App Passwords** in my Gmail and then create a new 
password *(this can only be done if you have already set up your 2-step verification; if not you will have to do it first)*.

Once you set up the name of the app and the type of computer where it's being accessed from, Gmail 
will then generate a password for you which you can then use in your code.

For I have put this in my envirnment variables file `.env` and made sure this is on my `.gitignore` file so my information is 
protected.  ***It is Highly reccomended to adhere to this practice in order to keep your persoanl information safe.***