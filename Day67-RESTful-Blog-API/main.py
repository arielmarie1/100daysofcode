from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
secret_key = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = secret_key
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)
Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class NewPostForm(FlaskForm):
    title = StringField(label='Blog Post Title', validators=[DataRequired()])
    subtitle = StringField(label='Subtitle', validators=[DataRequired()])
    author = StringField(label='Your Name', validators=[DataRequired()])
    img_url = StringField(label='Blog Image URL', validators=[DataRequired(), URL()])
    body = CKEditorField(label="Blog Content", validators=[DataRequired()])
    submit = SubmitField(label="Submit Post")


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    return render_template("post.html", post=requested_post)


@app.route('/new-post', methods=['GET', 'POST'])
def add_new_post():
    new_post_form = NewPostForm()
    if new_post_form.validate_on_submit():
        today_date = date.today().strftime("%B %d, %Y")
        with app.app_context():
            new_post = BlogPost(
                title=request.form.get("title"),
                subtitle=request.form.get("subtitle"),
                author=request.form.get("author"),
                img_url=request.form.get("img_url"),
                date=today_date,
                body=request.form.get("body"))
            db.session.add(new_post)
            db.session.commit()
        return render_template("make-post.html", form=new_post_form, post_added=True)
    return render_template('make-post.html', form=new_post_form, post_added=False)


@app.route('/edit/<int:post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    post_to_edit = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    edit_post_form = NewPostForm(obj=post_to_edit)
    if edit_post_form.validate_on_submit():
        post_to_edit.title = request.form.get("title")
        post_to_edit.subtitle=request.form.get("subtitle")
        post_to_edit.author=request.form.get("author")
        post_to_edit.img_url=request.form.get("img_url")
        post_to_edit.body=request.form.get("body")
        db.session.commit()
        return render_template("post.html", post=post_to_edit)
    return render_template("make-post.html", form=edit_post_form, edit_post=True)


@app.route('/delete/<int:post_id>', methods=["GET", "POST"])
def delete_post(post_id):
    post_to_delete = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
