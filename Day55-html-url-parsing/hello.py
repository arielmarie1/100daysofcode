from flask import Flask

app = Flask(__name__)
print(__name__)


def make_bold(function):
    def wrapper():
        return f"<b>" + function() + "</b>"
    return wrapper


def make_emphasis(function):
    def wrapper():
        return f"<em>" + function() + "</em>"
    return wrapper


def make_underline(function):
    def wrapper():
        return f"<u>" + function() + "</u>"
    return wrapper


@app.route("/")
def hello_world():
    return ('<h1 style="text-align: center">Hello, World!</h1>'
            '<p>This is a kitten.</p>'
            '<img src="https://smb.ibsrv.net/imageresizer/image/'
            'article_manager/1200x1200/20586/516506/heroimage0.327162001643150501.jpg" width=200>')


@app.route("/bye")
@make_bold
@make_emphasis
@make_underline
def say_bye():
    return "Bye!"


# Creating variable paths and converting user inputs
@app.route("/<name>/<int:number>")
def greet(name, number):
    return f"Hello, {name}, your favorite number is {number}!"


# Run in debug mode
if __name__ == "__main__":
    app.run(debug=True)
