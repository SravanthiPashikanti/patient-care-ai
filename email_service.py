import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import *

def send_email_to_doctor(patient_name, age, disease):
    try:
        subject = "⚠ Elder Patient Health Alert"
        
        body = f"""
Doctor Name : {DOCTOR_NAME}
Location    : {DOCTOR_PLACE}
Availability: {DOCTOR_TIMING}

---------------------------------
Patient Alert
---------------------------------
Patient Name : {patient_name}
Age          : {age}
Predicted Issue : {disease}

Please contact the patient immediately.
"""

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = DOCTOR_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print("Email Error:", e)
        return False
