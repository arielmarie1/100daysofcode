from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret_key'
Bootstrap5(app)
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
        print(all_books)
        return render_template("add.html", form=form, headers=formheaders, book_added=True)
    return render_template("add.html", form=form, headers=formheaders, book_added=False)


if __name__ == "__main__":
    app.run(debug=True)

