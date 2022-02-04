from email import message
import smtplib, ssl
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(email, tracker_id):
    sender = "yourqrcodekey@gmail.com"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(sender, "MyQRCodeKey")

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = email
    message["Subject"] = "Your QR Code Has Been Generated"
    body = """Your QR Code has been generated. Please find the attached QR Code.
    Please use the following tracker ID to track your QR Code: """ + str(tracker_id)
    message.attach(MIMEText(body, "plain"))

    filename = "qrcode.png"
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename= {filename}')

    message.attach(part)
    text = message.as_string()


    server.sendmail(sender, email, text)
    server.quit()