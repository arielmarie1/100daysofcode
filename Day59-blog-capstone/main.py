from flask import Flask, render_template
import requests

app = Flask(__name__)

blog_url = "https://api.npoint.io/b329384f235cf8d55795"
response = requests.get(blog_url)
all_posts = response.json()


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


@app.route("/contact")
def contact():
    return render_template("contact.html")


# Run in debug mode
if __name__ == "__main__":
    app.run(debug=True)
