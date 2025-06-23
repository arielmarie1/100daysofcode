from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'

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

# Create a new record
with app.app_context():
    book1 = Book(id=1, title='Harry Potter', author='J.K. Rowling', rating=9.3)
    # new_book = Book(title='Exhalation', author='Ted Chang', rating=9.4)
    db.session.add(book1)
    db.session.commit()

# Read all records
with app.app_context():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()

# Read a particular record by Query
with app.app_context():
    book = db.session.execute(
        db.select(Book).where(Book.title == 'Harry Potter')).scalar()

# Update a record by Query
# with app.app_context():
#     book_to_update = db.session.execute(db.select(Book).where(Book.title == 'Harry Potter')).scalar()
#     book_to_update.title = 'Harry Potter and the Chamber of Secrets'
#     db.session.commit()

# # Update a record by PRIMARY KEY
# book_id = 1
# with app.app_context():
#     book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
#     book_to_update.title = 'Harry Potter and the Goblet of Fire'
#     db.session.commit()

# # Delete a particular record by PRIMARY KEY
# book_id = 1
# with app.app_context():
#     book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
#     db.session.delete(book_to_delete)
#     db.session.commit()
