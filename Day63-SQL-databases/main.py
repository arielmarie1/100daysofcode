from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
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
all_books = []
formheaders = ["title", "author", "rating"]


class AddBookForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    author = StringField('Book Author', validators=[DataRequired()])
    rating = IntegerField('Rating 0-5',
                          validators=[InputRequired(),
                                      NumberRange(min=0, max=5)])
    submit = SubmitField('Submit')


@app.route('/')
def home():
    return render_template("index.html", headers=formheaders, all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddBookForm()

    if form.validate_on_submit():
        book_dict = {}
        for header in formheaders:
            book_dict[form[header].name] = form[header].data
        all_books.append(book_dict)
        print(book_dict.title)
        # # Create a new record
        # with app.app_context():
        #     book1 = Book(id=1, title='Harry Potter', author='J.K. Rowling', rating=9.3)
        #     # new_book = Book(title='Exhalation', author='Ted Chang', rating=9.4)
        #     db.session.add(book1)
        #     db.session.commit()
        return render_template("add.html", form=form, headers=formheaders, book_added=True)
    return render_template("add.html", form=form, headers=formheaders, book_added=False)


if __name__ == "__main__":
    app.run(debug=True)

