from flask import Flask, render_template
import requests


# run once to get the html
# data = requests.get("https://angelabauer.github.io/cv/").text
# with open("./templates/profile.html", "w") as file:
#     file.write(data)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()