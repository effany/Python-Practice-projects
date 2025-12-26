from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

def valid_login(username, password):
     return True if username and password else False

@app.route("/login", methods=["POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]
        print(username, password)
        if valid_login(username,password):
             return f"<h1>{username}{password}</h1>"
    else:
          error = "Invalud username/password"


