from flask import Flask, render_template, request, redirect, url_for, flash
from forms import QRInfo
import qrcode
from helper import send_email
import MySQLdb
import random

# Create the application instance
app = Flask(__name__, template_folder='templates')
# make a secret key
app.config['SECRET_KEY'] = 'mysecretkey'
# run app on ngrok
# Create a URL route in our application for "/"


@app.route('/' , methods=['GET', 'POST'])
def index():
    # validate the form and return the results
    form = QRInfo()
    
    if request.method == 'POST' and form.validate():
        website = form.website.data
        email = form.email.data

        # Create Cursur Object
        db = MySQLdb.connect(host="34.123.254.194", user="root", passwd="root", db="QRCodes")
        cursor = db.cursor()

        # Generate a random tracker id
        tracker_id = random.randint(1, 1000000)

        # Create a QR Code
        qr_code = qrcode.make('localhost:5000/site/' + str(tracker_id))
        type(qr_code)
        qr_code.save("qrcode.png")

        # Send the email
        send_email(email, tracker_id)

        # Insert the data into the database Tracker
        cursor.execute("""INSERT INTO Tracker (website, email, tracker, uses) VALUES (%s, %s, %s, %s)""", (website, email, tracker_id, 0))
        db.commit() 
        db.close()

        # Flash a message to the user
        flash('Your QR Code has been generated! Open your email to view.', 'success')
        return render_template('success.html', form=form)
    
    return render_template('index.html', form=form)


@app.route('/site/<tracker_id>')
def site(tracker_id):
    # open Tracker table & get the data
    db = MySQLdb.connect(host="34.123.254.194", user="root", passwd="root", db="QRCodes")
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM Tracker WHERE tracker = %s""", (tracker_id,))
    data = cursor.fetchone()
    db.close()
    
    data = list(data)
    
    # incremnt the uses and update the database
    uses = data[4]
    uses += 1

    db = MySQLdb.connect(host="34.123.254.194", user="root", passwd="root", db="QRCodes")
    cursor = db.cursor()
    cursor.execute("""UPDATE Tracker SET uses = %s WHERE tracker = %s""", (uses, tracker_id))
    db.commit()
    db.close()

    # redirect to the website
    return redirect(data[1])

@app.route('/track/<tracker_id>')
def track(tracker_id):

    # open Tracker table & get the data
    db = MySQLdb.connect(host="34.123.254.194", user="root", passwd="root", db="QRCodes")
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM Tracker WHERE tracker = %s""", (tracker_id,))
    data = cursor.fetchone()
    db.close()

    data = list(data)

    uses = data[4]

    return '<h1>This code has been used this QR Code {} times</h1>'.format(uses)

# If we're running in stand alone mode, run the application on a public IP
if __name__ == '__main__':
    app.run()
