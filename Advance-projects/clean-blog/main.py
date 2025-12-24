from flask import Flask, render_template
import requests
import datetime 


blog_api_url = "https://api.npoint.io/f3ea3004487949101703"
posts = requests.get(blog_api_url).json()
date = datetime.datetime.now()

app = Flask(__name__)

@app.route("/")
def home():
    global blog_api_url, posts, date
    return render_template("index.html", posts=posts, date=date)

@app.route("/blog/<int:id>")
def get_post(id):
    global posts, blog_api_url
    for post in posts:
        if post["id"] == id:
            post_title = post["title"]
            post_subtitle = post["subtitle"]
            post_body = post["body"]
    return render_template("post.html", id=id, post_title=post_title, post_subtitle = post_subtitle, post_body=post_body, post_date=date)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")




if __name__ == "__main__":
    app.run(debug=True)