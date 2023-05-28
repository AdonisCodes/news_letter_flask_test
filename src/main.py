from email.message import EmailMessage
import threading
import ssl
import smtplib
from flask import Flask, request, render_template, send_file
from cs50 import SQL

db = SQL("sqlite:///emails.db")

app = Flask(__name__, static_folder="static")

def send(bod, sub):
    host = "fernssimon1111@gmail.com"
    password = "bvjamqvrciujvskj"
    rec = db.execute("SELECT email FROM emails")
    subject = sub
    body = bod

    db.execute("INSERT INTO email_content (body, subject, views) VALUES (?, ?, 0)", bod, sub)

    context = ssl.create_default_context()
    for recipient in rec:
        email_address = recipient["email"]
        em = EmailMessage()
        em["From"] = host
        em["Subject"] = subject
        em.set_content(body, subtype="html")
        em["To"] = email_address

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as sept:
            sept.login(host, password)
            sept.send_message(em)

        print("Email sent to:", email_address)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    try:
        print(request.form.get("email"))
        db.execute("INSERT INTO emails (email) VALUES (?)", request.form.get("email"))
    except ValueError:
        return render_template("failed.html")
    return render_template("success.html")



@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "GET":
        return render_template("post.html")

    threading.Thread(target=send, args=(request.form.get("email"), request.form.get("subject"))).start()
    return render_template("stats.html")


if __name__ == "__main__":
    app.run()
