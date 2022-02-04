# PreBuild of the project
import qrcode
from helper import send_email
import random
import MySQLdb

url_request = input("Enter the website url: ")
email_request = input("Enter the email address: ")

# Connect to the database
db = MySQLdb.connect(host="34.123.254.194", user="root", passwd="root", db="QRCodes")
cursor = db.cursor()




tracker_id = random.randint(1, 1000000)

qr_code = qrcode.make('localhost:5000/site/' + str(tracker_id))
type(qr_code)
qr_code.save("qrcode.png")

send_email(email_request, tracker_id)

# Insert the data into the database Tracker
cursor.execute("""INSERT INTO Tracker (website, email, tracker, uses) VALUES (%s, %s, %s, %s)""", (url_request, email_request, tracker_id, 0))
db.commit()
print("Executed")
