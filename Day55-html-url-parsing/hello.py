from flask import Flask

app = Flask(__name__)
print(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/bye")
def say_bye():
    return "Bye"

# Creating variable paths and converting user inputs
@app.route("/<name>/<int:number>")
def greet(name, number):
    return f"Hello, {name}, your favorite number is {number}!"

# Run in debug mode
if __name__ == "__main__":
    app.run(debug=True)


