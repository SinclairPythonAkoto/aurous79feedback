Aurous79 Feedback

This is a simple web app for a shisha bar/restuarant.  The owner wanted to create a feedback form in order to obtain customer information in return for supplying a discount fro their next bill.

This web app allows the user to complete the feedback form in oredr to be sent an automated email for their discount.  The management can login to the Admin page and run reports on the different type of answers.  Management can also view the data in a graph format.

This Dash app is inside the Flask app with a prefixed pathname so I can only create one graph for the user to view.  Saying that, I managed to display all the graphs needed onto one page which made it easily accessible to view/analyze data from the database.

I have split up the database, and the graph functions into separate Python files and imported them into my main app.py file.  This is so that the code can be easily targeted if something goes wrong and that my main file hasn't got so much lines of code.  This can sometimes make it hard to find a line in a piece of code or easily get lost within several lines of code!

I have also just managed to create a mass emailing platform.  It has been done in such a way that the management can insert a name & email into a table to send mass emails from; or they can simply pick the list of emails collated from the feedback form.