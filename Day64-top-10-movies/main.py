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


## Test adding a new movie to database
# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, "
#                 "pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, "
#                 "Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )

# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()


@app.route("/")
def home():
    with app.app_context():
        movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars().all()
    return render_template("index.html", headers=form_headers, movies=movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovieForm()

    if form.validate_on_submit():
        # Create a new record
        with app.app_context():
            form_data = {f.name: f.data for f in form if f.name not in ["csrf_token", "submit"]}
            add_movie = Movie(**form_data)
            db.session.add(add_movie)
            db.session.commit()
        return render_template("add.html", form=form, headers=form_headers, book_added=True)
    return render_template("add.html", form=form, headers=form_headers, book_added=False)


if __name__ == '__main__':
    app.run(debug=True)
