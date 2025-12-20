from flask import Flask, render_template
import random
import datetime
import requests
import json


app = Flask(__name__)
agify_url = "https://api.agify.io/"
genderize_url = "https://api.genderize.io/"
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}

@app.route('/')
def home():
    random_num = random.randint(1,10)
    copy_right_year = datetime.datetime.now().year
    return render_template("index.html", num=random_num, year=copy_right_year)

@app.route('/guess/<name>')
def guess(name):
    gender_response = requests.get(f"{genderize_url}?name={name}", headers=headers)
    gender_data = gender_response.json()
    gender = gender_data["gender"]

    age_response = requests.get(f"{agify_url}?name={name}", headers=headers)
    age_data = age_response.json()["age"]
    name = name.capitalize()
    
    copy_right_year = datetime.datetime.now().year
    return render_template("index.html", gender=gender, age=age_data, name=name, year=copy_right_year)
    
@app.route('/blog/<num>')
def get_blog(num):
    blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts)



if __name__ == "__main__":
    app.run(debug=True)


