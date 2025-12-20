from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__": 
    app.run()


## in chrome in the console do document.body.contentEditable=true , then you can edit the website
## after editing, you can simply just save the page as html and put in your render folder




