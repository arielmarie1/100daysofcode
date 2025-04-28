from flask import Flask
from random import randint

app = Flask(__name__)

random_number = randint(0, 9)
print(random_number)


@app.route("/")
def guess_number():
    return ('<h1>Guess a number between 0 and 9</h1>'
            '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" width=200>')


# Creating variable paths and converting user inputs
@app.route("/<int:number>")
def game(number):
    if random_number > number:
        return ('<h1 style="color:purple">Too low, try again</h1>'
                '<img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif" width=200>')
    if random_number < number:
        return ('<h1 style="color:red">Too high, try again</h1>'
                '<img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif" width=200>')
    else:
        return ('<h1 style="color:green">You got it!</p>'
                '<img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif" width=200>')


# Run in debug mode
if __name__ == "__main__":
    app.run(debug=True)
