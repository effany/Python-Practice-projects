from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    img_url: Mapped[str] = mapped_column(String(500))
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250))
    has_toilet: Mapped[bool] = mapped_column(Boolean)
    has_wifi: Mapped[bool] = mapped_column(Boolean)
    has_sockets: Mapped[bool] = mapped_column(Boolean)
    can_take_calls: Mapped[bool] = mapped_column(Boolean)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
    likes: Mapped[int] = mapped_column(nullable=True)

prague_cafes = [
    {
        "name": "Café Louvre",
        "map_url": "https://goo.gl/maps/CafeLouvre",
        "img_url": "https://images.unsplash.com/photo-1554118811-1e0d58224f24",
        "location": "Národní 22, Prague 1",
        "seats": "150",
        "has_toilet": True,
        "has_wifi": True,
        "has_sockets": True,
        "can_take_calls": True,
        "coffee_price": "80 Kč"
    },
    {
        "name": "Kavárna Slavia",
        "map_url": "https://goo.gl/maps/KavarnaSlavia",
        "img_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb",
        "location": "Smetanovo nábřeží 2, Prague 1",
        "seats": "120",
        "has_toilet": True,
        "has_wifi": False,
        "has_sockets": False,
        "can_take_calls": False,
        "coffee_price": "85 Kč"
    },
    {
        "name": "EMA Espresso Bar",
        "map_url": "https://goo.gl/maps/EMAEspresso",
        "img_url": "https://images.unsplash.com/photo-1442512595331-e89e73853f31",
        "location": "Národní 17, Prague 1",
        "seats": "30",
        "has_toilet": True,
        "has_wifi": True,
        "has_sockets": True,
        "can_take_calls": True,
        "coffee_price": "65 Kč"
    },
    {
        "name": "Manifesto Market",
        "map_url": "https://goo.gl/maps/ManifestoMarket",
        "img_url": "https://images.unsplash.com/photo-1559496417-e7f25c24bd83",
        "location": "Wenceslas Square, Prague 1",
        "seats": "200",
        "has_toilet": True,
        "has_wifi": True,
        "has_sockets": False,
        "can_take_calls": True,
        "coffee_price": "70 Kč"
    },
    {
        "name": "Café Savoy",
        "map_url": "https://goo.gl/maps/CafeSavoy",
        "img_url": "https://images.unsplash.com/photo-1521017432531-fbd92d768814",
        "location": "Vítězná 5, Prague 5",
        "seats": "80",
        "has_toilet": True,
        "has_wifi": True,
        "has_sockets": True,
        "can_take_calls": False,
        "coffee_price": "90 Kč"
    },
    {
        "name": "Můj šálek kávy",
        "map_url": "https://goo.gl/maps/MujSalekKavy",
        "img_url": "https://images.unsplash.com/photo-1511920170033-f8396924c348",
        "location": "Křižíkova 105, Prague 8",
        "seats": "40",
        "has_toilet": True,
        "has_wifi": True,
        "has_sockets": True,
        "can_take_calls": True,
        "coffee_price": "60 Kč"
    }
]

with app.app_context():
    db.create_all()  # Create the tables if they don't exist
    for cafe_data in prague_cafes:
        # Check if cafe already exists
        existing_cafe = db.session.execute(
            db.select(Cafe).where(Cafe.name == cafe_data["name"])
        ).scalar_one_or_none()
        
        if not existing_cafe:
            new_cafe = Cafe(**cafe_data)
            db.session.add(new_cafe)
            print(f"Added: {cafe_data['name']}")
        else:
            print(f"Already exists: {cafe_data['name']}")
    
    db.session.commit()
    print("\nAll Prague cafes have been added to the database!")
