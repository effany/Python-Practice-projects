from flask import Flask
import random

app = Flask(__name__)

random_num = None

@app.route("/")
def greeting_rules():
    global random_num
    random_num = generate_ramdom_number()
    print(random_num)
    return '<h1>I am thinking of a number between 0 and 10...</h1>'\
            '<img width=500 src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWt6dnRiazh0eHNmNmE0djh1eXRwZjMzanhmenB2dHNyd2UycDQxcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qLRB2YK95yMpYc5HZD/giphy.gif"</img>'

def generate_ramdom_number():
    return random.randint(0,10)


@app.route("/<int:number>")
def check_answer(number):
    global random_num
    if number < random_num:
        return '<h1>No No, too low</h1>' \
                '<img width=500 src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExYmVmb3lsbzdoNXJmdnlveGU3NWxlNm9qeWI4cHdzMGk2bmE0cmZlYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/mCHQUhwwy1rKP3D04W/giphy.gif"></img>'
    elif number > random_num:
        return '<h1>Too high </h1>' \
                '<img width=500 src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWliNWYxY25ib3J4bnc1Z2RwdHRtcnFyMzc0djJsajJwOTQ4cmZhZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XtD5Nwjxsxw0E/giphy.gif"></img>'
    elif number == random_num:
        return '<h1>Eactly RIGHT!</h1>' \
                '<img width=500 src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3AwaDR0ODkyMTZzbTA0OGU3OGh6d285ZzVneHFwcGNveG91aTVtaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/IzuWNg7cJD4mxDmO6g/giphy.gif"></img>'