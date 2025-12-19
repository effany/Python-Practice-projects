from flask import Flask

# flask run to start running 

def make_bold(function):
    def boldden(*args, **kwargs):
        return f"<b>{function(*args, **kwargs)}</b>"
    return boldden

def make_emphasis(function):
    def emphasis(*args, **kwargs):
        return f"<em>{function()}</em>"
    return emphasis

def make_underline(function):
    def underline(*args, **kwargs):
        return f"<u>{function()}</u>"
    return underline


app = Flask(__name__)

@app.route("/")
def hello_world():
    return '<h1 style="text-align: center">Hello, World!</h1>' \
            '<p>This is a paragraph</p>' \
            '<img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnY1bHN3cGJqYWZlemY5a2JtNWpiM2g5Yzc5NGtlZXNjd3h0MTR5ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wHc92cHADhpLi/giphy.gif" width=200></img>'


@app.route("/bye")
@make_bold
@make_emphasis
@make_underline
def say_bye():
    return "Bye"

@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"Hello there {name}, your lucky number is {number}"

if __name__ == " __main__":
    app.run(debug=True)