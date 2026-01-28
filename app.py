from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import smtplib
from email.message import EmailMessage

# ===============================
# APP INITIALIZATION
# ===============================
app = Flask(__name__)
CORS(app)

# ===============================
# Doctor Details
# ===============================
DOCTOR_NAME = "Dr. Sravanthi"
DOCTOR_EMAIL = "22b61a7247@nmrec.edu.in"
DOCTOR_LOCATION = "Narapally"
DOCTOR_TIMING = "24/7"

# ===============================
# Email Configuration (Gmail)
# ===============================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "sravanthipashikanti2502@gmail.com"
SENDER_PASSWORD = "lwxhqkwnqoaavyxc"   # Gmail App Password

# ===============================
# HOME / DASHBOARD ROUTE
# ===============================
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# ===============================
# CONTACT DETAILS API
# ===============================
@app.route("/contact", methods=["GET"])
def contact():
    return jsonify({
        "doctor_name": DOCTOR_NAME,
        "doctor_email": DOCTOR_EMAIL,
        "location": DOCTOR_LOCATION,
        "timing": DOCTOR_TIMING
    })

# ===============================
# EMAIL SENDING FUNCTION
# ===============================
def send_email_to_doctor(patient, age, disease):
    msg = EmailMessage()
    msg["Subject"] = "🚨 AI Patient Alert"
    msg["From"] = SENDER_EMAIL
    msg["To"] = DOCTOR_EMAIL

    msg.set_content(f"""
Doctor Alert from Agentic AI System

Patient Name : {patient}
Age          : {age}
Predicted Condition : {disease}

Please review immediately.
""")

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()

# ===============================
# PREDICTION API
# ===============================
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    name = data.get("name")
    age = int(data.get("age"))
    symptoms = data.get("symptoms", [])

    email_sent = False

    # -------------------------------
    # Simple Rule-Based Prediction
    # -------------------------------
    if "skin_rash" in symptoms or "itching" in symptoms:
        disease = "Skin Allergy"
        confidence = 0.85
    elif "chest_pain" in symptoms or "breathlessness" in symptoms:
        disease = "Possible Heart Issue"
        confidence = 0.90
    else:
        disease = "General Health Issue"
        confidence = 0.65

    # -------------------------------
    # AGE-BASED ALERT (30+ years)
    # -------------------------------
    if age >= 30:
        send_email_to_doctor(name, age, disease)
        email_sent = True
        alert = "🚨 Doctor notified via email (Age 30+)"
    else:
        alert = "No critical alert"

    return jsonify({
        "predicted_disease": disease,
        "confidence": confidence,
        "alert": alert,
        "email_sent": email_sent
    })

# ===============================
# RUN FLASK SERVER
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)







