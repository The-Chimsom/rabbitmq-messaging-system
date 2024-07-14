# messaging_system/app.py
from flask import Flask, request
import smtplib
import logging
from datetime import datetime
from messaging_system.celery import celery

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery.conf.update(app.config)

logging.basicConfig(filename='messaging_system.log', level=logging.INFO)

@celery.task
def send_email(recipient):
    smtp_server = "smtp.example.com"
    smtp_port = 587
    smtp_user = "your_email@example.com"
    smtp_password = "your_password"

    message = f"Subject: Test Email\n\nThis is a test email to {recipient}"

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipient, message)

@app.route('/', methods=['GET'])
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')
    
    if sendmail:
        send_email.delay(sendmail)
        return f"Email to {sendmail} queued for sending."
    
    if talktome:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"Current time logged: {current_time}")
        return f"Current time {current_time} logged."

    return "Please provide a valid parameter."

if __name__ == '__main__':
    app.run(debug=True)
