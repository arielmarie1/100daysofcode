from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# Creating variable paths and converting user inputs
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def receive_data():
    username = request.form['username']
    password = request.form['password']
    return f"<h1>Name: {username} Password: {password} </h1>"


# Run in debug mode
if __name__ == "__main__":
    app.run(debug=True)
