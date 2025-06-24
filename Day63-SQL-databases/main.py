from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange, InputRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret_key'
bootstrap = Bootstrap(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book-collection.db'

# Create and Initialize extension
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()


# Create website form
formheaders = ["title", "author", "rating"]


# Add new book to Library
class AddBookForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    author = StringField('Book Author', validators=[DataRequired()])
    rating = FloatField('Rating 0-10',
                          validators=[InputRequired(),
                                      NumberRange(min=0, max=10)])
    submit = SubmitField('Submit')


# Edit rating of existing book in Library
class EditRatingForm(FlaskForm):
    edit_rating = FloatField('Update Rating 0-10:',
                          validators=[InputRequired(),
                                      NumberRange(min=0, max=10)])
    submit = SubmitField('Change Rating')


@app.route('/')
def home():
    with app.app_context():
        books = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
    return render_template("index.html", headers=formheaders, all_books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddBookForm()

    if form.validate_on_submit():
        book_dict = {}
        for header in formheaders:
            book_dict[form[header].name] = form[header].data
        # Create a new record
        with app.app_context():
            book = Book(title=book_dict["title"], author=book_dict["author"], rating=book_dict["rating"])
            db.session.add(book)
            db.session.commit()
        return render_template("add.html", form=form, headers=formheaders, book_added=True)
    return render_template("add.html", form=form, headers=formheaders, book_added=False)


@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    with app.app_context():
        books = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
    edit_form = EditRatingForm()
    if edit_form.validate_on_submit():
        with app.app_context():
            book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
            book_to_update.rating = edit_form["edit_rating"].data
            db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=edit_form, all_books=books, book_id=book_id)


if __name__ == "__main__":
    app.run(debug=True)
