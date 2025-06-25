from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, URLField
from wtforms.validators import DataRequired, InputRequired, NumberRange, URL
import requests
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)

# The Movie Database API
TMDB_API_KEY = os.getenv("API_KEY")


# CREATE DB
class Base(DeclarativeBase):
    pass


# Create and Initialize extension
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[str] = mapped_column(String(4), nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String, nullable=True)
    img_url: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()


# CREATE FORM
class MovieTitleForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


form_headers = ["title", "year", "description", "rating", "ranking", "review", "img_url"]


class AddMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    rating = FloatField('Imdb Rating', validators=[InputRequired(), NumberRange(min=0, max=10)])
    ranking = IntegerField('Ranking', validators=[InputRequired()])
    review = StringField('My Review', validators=[DataRequired()])
    img_url = URLField('Image URL', validators=[URL(), DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    with app.app_context():
        movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars().all()
    return render_template("index.html", headers=form_headers, movies=movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = MovieTitleForm()
    if form.validate_on_submit():
        parameters = {
            "api_key": TMDB_API_KEY,
            "query": form.title.data
        }
        response = requests.get("https://api.themoviedb.org/3/search/movie", params=parameters)
        response.raise_for_status()
        data = response.json()
        search_results = data["results"]
        return render_template("select.html", results=search_results)
    return render_template("add.html", form=form)


@app.route("/select/<int:api_movie_id>", methods=["GET", "POST"])
def select(api_movie_id):
    url = f"https://api.themoviedb.org/3/movie/{api_movie_id}"
    response = requests.get(url, params={"api_key": TMDB_API_KEY})
    response.raise_for_status()
    movie = response.json()
    new_movie = Movie(
        title=movie["title"],
        year=movie["release_date"][:4],
        description=movie["overview"],
        rating=movie["vote_average"],
        ranking=0,
        review="",
        img_url=f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
    )
    with app.app_context():
        db.session.add(new_movie)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:movie_id>", methods=["GET", "POST"])
def delete(movie_id):
    with app.app_context():
        movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
        db.session.delete(movie_to_delete)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    with app.app_context():
        movie_to_edit = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
        form = AddMovieForm(obj=movie_to_edit)
        if form.validate_on_submit():
            form.populate_obj(movie_to_edit)
            db.session.commit()
            return redirect(url_for("home"))
        return render_template("edit.html", form=form, headers=form_headers, movie_id=movie_id)


if __name__ == '__main__':
    app.run(debug=True)
