from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from edit_form import EditForm
from add_movie_form import AddMoiveForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

load_dotenv()

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-movies-collection.db"
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    year: Mapped[int] 
    description: Mapped[str] 
    rating: Mapped[float | None] = mapped_column(nullable=True)
    ranking: Mapped[int | None] = mapped_column(nullable=True)
    review: Mapped[str | None] = mapped_column(nullable=True)
    img_url: Mapped[str]

with app.app_context():
    db.create_all()

#     # add new entry to db 
#     new_movie = Movie(
#         title="Phone Booth",
#         year=2002,
#         description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#         rating=7.3,
#         ranking=10,
#         review="My favourite character was the caller.",
#         img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#     )

#     second_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )
#     db.session.add(new_movie)
#     db.session.add(second_movie)
#     db.session.commit()

@app.route("/")
def home():
    global all_movies
    result = db.session.execute(db.select(Movie).order_by(Movie.ranking))
    all_movies = result.scalars().all()
    return render_template("index.html", all_movies = all_movies)

@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit_movie(id):
    form = EditForm()
    movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()

    if form.validate_on_submit():
        if form.rating.data:
            movie_to_update.rating = form.rating.data
        if form.review.data:
            movie_to_update.review = form.review.data
        if form.ranking.data:
            movie_to_update.ranking = form.ranking.data
        
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template('edit.html', movie=movie_to_update, form=form)    

@app.route("/delete/<int:id>")  
def delete_movie(id):
    movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
    db.session.delete(movie_to_delete)
    db.session.commit()

    return redirect(url_for('home'))

@app.route("/add", methods=["POST", "GET"])
def add_movie():
    form = AddMoiveForm()
    if form.validate_on_submit():
        title = form.movie_title.data
        api_key = os.environ.get("API_ACCESS_TOKEN")
        headers = {
            "accept": "application/json", 
            "Authorization": f"Bearer {api_key}"
        }
        params = {
            "query": title,
            "include_adult": "false"
        }
        response = requests.get("https://api.themoviedb.org/3/search/movie", params=params, headers=headers)
        data = response.json()["results"]
        return render_template('select.html', movies = data)
    
    return render_template("add.html", form=form)

@app.route("/select/<int:id>", methods=["POST", "GET"])
def select_movie(id):
    api_key = os.environ.get("API_ACCESS_TOKEN")
    headers = {
            "accept": "application/json", 
            "Authorization": f"Bearer {api_key}"
        }
    url = f"https://api.themoviedb.org/3/movie/{id}"
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Check if movie already exists
    existing_movie = db.session.execute(db.select(Movie).where(Movie.title == data["title"])).scalar()
    if existing_movie:
        # Movie already exists, redirect to edit it
        return redirect(url_for('edit_movie', id=existing_movie.id))

    new_movie_to_add = Movie(
         title=data["title"],
         year=data["release_date"],
         description=data['overview'],
         rating=None,
         ranking=None,
         review=None,
         img_url=f"https://image.tmdb.org/t/p/w500{data["poster_path"]}"
     )
    
    db.session.add(new_movie_to_add)
    db.session.commit()
    
    # Redirect to edit page instead of rendering directly
    return redirect(url_for('edit_movie', id=new_movie_to_add.id))

if __name__ == '__main__':
    app.run(debug=True)
