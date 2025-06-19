from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField, URLField
from wtforms.validators import DataRequired, NumberRange, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

cafeformheaders = ["cafe", "location", "open_time", "close_time",
                   "coffee_rating", "wifi_rating", "power_rating"]


class CafeForm(FlaskForm):
    cafe = StringField(
        'Cafe name',
        validators=[DataRequired()])
    location = URLField(
        'Location URL',
        validators=[DataRequired(), URL()])
    open_time = DateTimeField(
        'Opening time',
        format="%I %p",
        render_kw={"placeholder": "ex. 9 AM"},
        validators=[DataRequired()])
    close_time = DateTimeField(
        'Closing time',
        format="%I %p",
        render_kw={"placeholder": "ex. 10 PM"},
        validators=[DataRequired()])
    coffee_rating = IntegerField(
        'Coffee Rating 0-5',
        validators=[DataRequired(),
                    NumberRange(min=0, max=5)])
    wifi_rating = IntegerField(
        'Wifi Rating 0-5',
        validators=[DataRequired(),
                    NumberRange(min=0, max=5)])
    power_rating = IntegerField(
        'Power Outlet Rating 0-5',
        validators=[DataRequired(),
                    NumberRange(min=0, max=5)])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add')
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
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
