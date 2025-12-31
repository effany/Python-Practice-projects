from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.sql import func

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns: 
            dictionary[column.name] = getattr(self, column.name)
        
        return dictionary


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random_cafe():
    random_cafe = db.session.execute(db.select(Cafe).order_by(func.random())).scalar()
    # return jsonify(
    #     can_take_calls = random_cafe.can_take_calls, 
    #     coffee_price = random_cafe.coffee_price,
    #     has_sockets = random_cafe.has_sockets, 
    #     has_toilet = random_cafe.has_toilet, 
    #     has_wifi = random_cafe.has_wifi, 
    #     id = random_cafe.id, 
    #     img_url = random_cafe.img_url, 
    #     location = random_cafe.location, 
    #     map_url = random_cafe.map_url, 
    #     name = random_cafe.name, 
    #     seats = random_cafe.seats
    # ) 
    return jsonify(cafe=random_cafe.to_dict())

# HTTP GET - Read Record
@app.route("/all", methods=["GET"])
def get_all_cafes():
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
    cafes_list = [cafe.to_dict() for cafe in cafes]
    return jsonify(cafes=cafes_list)
# HTTP GET - Read Record
@app.route("/search")
def search_cafes():
    query_location = request.args.get("loc")
    cafes_db = db.session.execute(db.select(Cafe).where(Cafe.location == query_location.capitalize())).scalars().all()
    if cafes_db:
        cafes_result = [cafe.to_dict() for cafe in cafes_db]
        return jsonify(cafes=cafes_result)
    else:
        return jsonify(error={"Not Found": "Sorry we don't have cafes in that location"})


# HTTP POST - Create Record

@app.route("/new", methods=["POST"])
def add_new_cafe():
    query = request.form 
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        has_sockets=bool(request.form.get("has_sockets")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        coffee_price=request.form.get("coffee_price")
    )

    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully add cafe to db"})

# HTTP PUT/PATCH - Update Record

@app.route("/update-price/<int:id>", methods=["PATCH"])
def update_price(id):
    try:
        cafe_to_update = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()
        new_price = request.args.get("new_price")
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"Success": "Successfully update the cafe"})
    except AttributeError:
        return jsonify(response={"Error": "The cafe doesn't exist"})

# HTTP DELETE - Delete Record


@app.route("/report-closed/<int:id>", methods=["DELETE"])
def delete_cafe(id):
    cafe_to_delete = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey" and cafe_to_delete:
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(response = {"Success": "Successfully delete the cafe"})
    else:
        return jsonify(response={"Error": "Ooops there's an error. Try again"})
    
if __name__ == '__main__':
    app.run(debug=True)
