from flask import Flask, render_template

app = Flask(__name__)


# Creating variable paths and converting user inputs
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post")
def post():
    return render_template("post.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# Run in debug mode
if __name__ == "__main__":
    app.run(debug=True)
