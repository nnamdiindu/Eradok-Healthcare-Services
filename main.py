from flask import Flask, render_template, request, redirect, url_for
import smtplib
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=["POST", "GET"])
def make_appointment():
    if request.method == "POST":
        name = request.form.get("customer_name")
        phone = request.form.get("customer_phone")
        email = request.form.get("customer_email")
        date = request.form.get("date")
        time = request.form.get("time")
        message = request.form.get("message")

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=os.environ.get("MY_EMAIL"), password=os.environ.get("PASSWORD"))
            connection.sendmail(
                from_addr=os.environ.get("MY_EMAIL"),
                to_addrs=os.environ.get("RECEIVER"),
                msg=f"Subject:Appointment Notification\n\n"
                    f"Name: {name}\nPhone Number: {phone}\n"
                    f"Email: {email}\n"
                    f"Proposed Appointment Date: {date}\n"
                    f"Time: {time}\n"
                    f"{message}"
            )
            return render_template("success.html")


        # from twilio.rest import Client
        #
        # account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        # auth_token = os.environ.get("TWILIO_ACCOUNT_AUTH")
        # client = Client(account_sid, auth_token)
        #
        # message = client.messages.create(
        #     from_="+19032900154",
        #     body=f"Name: {name}\n"
        #          f"Email: {email}\n"
        #          f"Phone: {phone}\n"
        #          f"Date: {date}\n"
        #          f"Time: {time}\n"
        #          f"Message: {message}",
        #     to="+2348073138700"
        # )
        #
        # print(message.sid)
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)