from flask import Flask, render_template, request, redirect, url_for
from forms import QRInfo
import pyqrcode
from helper import send_email
import MySQLdb
from flask_ngrok import run_with_ngrok

# Create the application instance
app = Flask(__name__, template_folder='templates')
# make a secret key
app.config['SECRET_KEY'] = 'mysecretkey'
# run app on ngrok
run_with_ngrok(app)
# Create a URL route in our application for "/"
@app.route('/')
def index():
    # validate the form and return the results
    form = QRInfo()
    
    if request.method == 'POST' and form.validate():
        website = form.website.data
        email = form.email.data
        print("complete")
    return render_template('index.html', form=form)

@app.route('/site/<tracker_id>')
def site(tracker_id):
    # open Tracker table & get the data
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="QRCodes")
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM tracker WHERE tracker = %s""", (tracker_id,))
    data = cursor.fetchone()
    db.close()
    
    data = list(data)
    
    # incremnt the uses and update the database
    uses = data[4]
    uses += 1

    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="QRCodes")
    cursor = db.cursor()
    cursor.execute("""UPDATE tracker SET uses = %s WHERE tracker = %s""", (uses, tracker_id))
    db.commit()
    db.close()

    # redirect to the website
    return redirect(data[1])

@app.route('/track/<tracker_id>')
def track(tracker_id):

    # open Tracker table & get the data
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="QRCodes")
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM tracker WHERE tracker = %s""", (tracker_id,))
    data = cursor.fetchone()
    db.close()

    data = list(data)

    uses = data[4]

    return '<h1>This code has been used this QR Code {} times</h1>'.format(uses)

# If we're running in stand alone mode, run the application on a public IP
if __name__ == '__main__':
    app.run()
