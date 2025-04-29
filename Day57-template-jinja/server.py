from flask import Flask, render_template
import random
from datetime import datetime
import requests

app = Flask(__name__)


def guess_age(name: str) -> dict:
    url = "https://api.agify.io"
    params = {"name": name}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    age = data["age"]
    return age


def guess_gender(name: str) -> dict:
    url = "https://api.genderize.io"
    params = {"name": name}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    gender = data["gender"]
    return gender


@app.route('/')
def home():
    random_number = random.randint(1, 10)
    current_year = datetime.now().year
    return render_template('index.html', num=random_number, year=current_year)


@app.route('/guess/<name>/')
def guess(name):
    age = guess_age(name)
    gender = guess_gender(name)
    current_year = datetime.now().year
    return render_template("guess.html", name=name, age=age, gender=gender, year=current_year)


@app.route("/blog/<num>")
def get_blog(num):
    blog_url = "https://api.npoint.io/9236954c6c21b76094cf"
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts)


if __name__ == '__main__':
    app.run(debug=True)
