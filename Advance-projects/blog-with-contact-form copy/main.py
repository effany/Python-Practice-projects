from flask import Flask, render_template, request
import requests
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
my_email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

app = Flask(__name__)

@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

@app.route("/form-entry", methods=["POST"])
def receive_data():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]

    email_message = f"from {name}, phone: {phone}, email: {email} message: {message}"
    print(name, email, phone, message)
    send_email(email_message)
    return "Successfully submit your form!"

def send_email(message):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=my_email, 
                            msg=f"Subject: You got a new message!\n\n{message}"
                            )

if __name__ == "__main__":
    app.run(debug=True, port=5001)
