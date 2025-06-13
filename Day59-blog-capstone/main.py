from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)

blog_url = "https://api.npoint.io/b329384f235cf8d55795"
response = requests.get(blog_url)
all_posts = response.json()

# Loading email
load_dotenv()
my_email = os.getenv("MY_EMAIL")
password = os.getenv("OTP")

# Creating variable paths and converting user inputs
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", posts=all_posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/<int:post_id>")
def post(post_id):
    return render_template("post.html", posts=all_posts, post_id=post_id)


@app.route("/contact", methods=["GET", "POST"])
def receive_data():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        # Email message
        msg = EmailMessage()
        msg['From'] = email
        msg['To'] = my_email
        msg["Subject"] = "Contact Form - Ariel's Blog"
        msg.set_content(f"Name: {name}\nEmail: {email}\nPhone number: {phone}\nMessage: {message}")

        # Sending email
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.send_message(msg)

        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


# Run in debug mode
if __name__ == "__main__":
    app.run(debug=True)
