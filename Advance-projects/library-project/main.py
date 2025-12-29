from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
## cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

app = Flask(__name__)

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)

class Books(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str] = mapped_column(String(50))
    rating: Mapped[float] = mapped_column(Float)

with app.app_context():
    db.create_all()

all_books = []

@app.route('/')
def home():
    global all_books
    result = db.session.execute(db.select(Books).order_by(Books.title))
    all_books = result.scalars().all()
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["Post", "Get"])
def add():
     return render_template('add.html')

@app.route("/form_entry", methods=["Post"])
def receive_data():
    book_name = request.form["book-name"]
    book_author = request.form["book-author"]
    rating = request.form["rating"]
    data = {"title": book_name, "author": book_author, "rating": rating}
    #all_books.append(data)
    book = Books(
        title = book_name,
        author = book_author,
        rating = rating
    )
    db.session.add(book)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit_book(id):
    book_to_update = db.session.execute(db.select(Books).where(Books.id == id)).scalar()
    id = book_to_update.id
    title = book_to_update.title
    author = book_to_update.author
    rating = book_to_update.rating

    if request.method == "POST":
        new_rating = request.form["score"]
        book_to_update.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit.html", id = id, title=title, author=author, rating=rating)

@app.route("/delete/<int:id>")
def delete_book(id):
    book_to_delete = db.session.execute(db.select(Books).where(Books.id == id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit() 
    
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

'''

Create A New Record
with app.app_context():
    new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
    db.session.add(new_book)
    db.session.commit()
NOTE: When creating new records, the primary key fields is optional. you can also write:

new_book = Book(title="Harry Potter", author="J. K. Rowling", rating=9.3)

the id field will be auto-generated.



Read All Records
with app.app_context():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()
To read all the records we first need to create a "query" to select things from the database. When we execute a query during a database session we get back the rows in the database (a Result object). We then use scalars() to get the individual elements rather than entire rows.





Read A Particular Record By Query
with app.app_context():
    book = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
To get a single element we can use scalar() instead of scalars().



Update A Particular Record By Query
with app.app_context():
    book_to_update = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
    book_to_update.title = "Harry Potter and the Chamber of Secrets"
    db.session.commit() 


Update A Record By PRIMARY KEY
book_id = 1
with app.app_context():
    book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    # or book_to_update = db.get_or_404(Book, book_id)  
    book_to_update.title = "Harry Potter and the Goblet of Fire"
    db.session.commit()  
Flask-SQLAlchemy also has some handy extra query methods like get_or_404() that we can use. Since Flask-SQLAlchemy version 3.0 the previous query methods like Book.query.get() have been deprecated



Delete A Particular Record By PRIMARY KEY
book_id = 1
with app.app_context():
    book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    # or book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
You can also delete by querying for a particular value e.g. by title or one of the other properties. Again, the get_or_404() method is quite handy.
'''