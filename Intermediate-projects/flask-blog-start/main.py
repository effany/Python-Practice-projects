from flask import Flask, render_template
import requests


app = Flask(__name__)

url = "https://api.npoint.io/c790b4d5cab58020d391"
posts = requests.get(url).json()

@app.route('/')
def home():
    global url, posts
    return render_template("index.html", posts = posts)

@app.route('/blog/<int:id>')
def get_post(id):
    global url, posts

    for post in posts:
        if post["id"] == id:
            post_title = post["title"]
            post_body = post["body"]
            post_subtitle = post["subtitle"]

    return render_template("post.html", id=id, post_title=post_title, post_body=post_body, post_subtitle=post_subtitle)


if __name__ == "__main__":
    app.run(debug=True)
