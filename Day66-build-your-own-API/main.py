from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random as r

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


def to_dict(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    with app.app_context():
        cafes = db.session.execute(db.select(Cafe)).scalars().all()
        random_cafe = r.choice(cafes)
        return jsonify(cafe=to_dict(random_cafe))


@app.route("/all")
def get_all_cafes():
    with app.app_context():
        cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
        all_cafes = [to_dict(cafe) for cafe in cafes]
        return jsonify(cafes=all_cafes)


@app.route("/search")
def find_cafe():
    loc = request.args.get("loc")
    with app.app_context():
        cafes = db.session.execute(db.select(Cafe).where(Cafe.location == loc)).scalars().all()
        all_cafes = [to_dict(cafe) for cafe in cafes]
    if all_cafes:
        return jsonify(cafes=all_cafes)
    else:
        statement = "Sorry, we don't have a cafe at that location"
        return jsonify(error=statement), 404


@app.route("/add", methods=["POST"])
def add_cafe():
    cafe = Cafe()
    cafe.name = request.form.get("name")
    cafe.map_url = request.form.get("map_url")
    cafe.img_url = request.form.get("img_url")
    cafe.location = request.form.get("location")
    cafe.seats = request.form.get("seats")
    cafe.has_toilet = request.form.get("has_toilet")
    cafe.has_wifi = request.form.get("has_wifi")
    cafe.has_sockets = request.form.get("has_sockets")
    cafe.can_take_calls = request.form.get("can_take_calls")
    cafe.coffee_price = request.form.get("coffee_price")

    db.session.add(cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added cafe"})


if __name__ == '__main__':
    app.run(debug=True)
