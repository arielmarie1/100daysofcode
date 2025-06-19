from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField, URLField
from wtforms.validators import DataRequired, NumberRange, URL, InputRequired
from datetime import datetime
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

cafeformheaders = ["cafe", "location", "open_time", "close_time",
                   "coffee_rating", "wifi_rating", "power_rating"]


def convert_rating(value, emoji):
    try:
        value = int(value)
        if value == 0:
            return "✘"
        return emoji * value
    except (ValueError, TypeError):
        return "✘"


class CafeForm(FlaskForm):
    cafe = StringField(
        'Cafe name',
        validators=[DataRequired()])
    location = URLField(
        'Location URL',
        validators=[DataRequired(), URL()])
    open_time = StringField(
        'Opening time',
        render_kw={"placeholder": "ex. 9AM"},
        validators=[DataRequired()])
    close_time = StringField(
        'Closing time',
        render_kw={"placeholder": "ex. 10PM"},
        validators=[DataRequired()])
    coffee_rating = IntegerField(
        'Coffee Rating 0-5',
        validators=[InputRequired(),
                    NumberRange(min=0, max=5)])
    wifi_rating = IntegerField(
        'Wifi Rating 0-5',
        validators=[InputRequired(),
                    NumberRange(min=0, max=5)])
    power_rating = IntegerField(
        'Power Outlet Rating 0-5',
        validators=[InputRequired(),
                    NumberRange(min=0, max=5)])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = []
        for header in cafeformheaders:
            cafe = form[header].data
            if header == "coffee_rating":
                cafe = convert_rating(cafe, "☕")
            if header == "wifi_rating":
                cafe = convert_rating(cafe, "💪")
            if header == "power_rating":
                cafe = convert_rating(cafe, "🔌")
            new_cafe.append(cafe)
        # Add new line if necessary
        with open("cafe-data.csv", "rb+") as f:
            f.seek(-1, 2)  # Go to the last byte of the file
            last_char = f.read(1)
            if last_char != b'\n':
                f.write(b'\n')  # Only add a newline if it's missing

        with open("cafe-data.csv", mode="a", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(new_cafe)

    return render_template('add.html', form=form, headers=cafeformheaders)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        cafes = []
        csv_headers = next(csv_data)  # first row
        for row in csv_data:
            cafe_dict = dict(zip(csv_headers, row))
            cafes.append(cafe_dict)
    return render_template('cafes.html', cafes=cafes, headers=csv_headers)


if __name__ == '__main__':
    app.run(debug=True)
