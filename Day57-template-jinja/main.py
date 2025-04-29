from flask import Flask, render_template
import requests


app = Flask(__name__)

@app.route('/posts')
def home():
    blog_url = "https://api.npoint.io/9236954c6c21b76094cf"
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template("index.html", posts=all_posts)

@app.route('/posts/<int:post_id>')
def get_blog(post_id):


if __name__ == "__main__":
    app.run(debug=True)
