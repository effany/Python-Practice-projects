from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, abort, session
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.sql import func
from functools import wraps
from flask_bootstrap import Bootstrap5
from werkzeug.security import generate_password_hash, check_password_hash
from form import NewUser, LoginForm, ApiKeyForm, EditForm
import os
from dotenv import load_dotenv
import random
import string
import secrets
import pyperclip
from unidecode import unidecode

load_dotenv()

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
db = SQLAlchemy(model_class=Base)
db.init_app(app)
bootstrap = Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)



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

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] 
    api_key: Mapped[str] = mapped_column(nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()

def user_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

with app.app_context():
    db.create_all()


# user interactions

@app.route('/')
def home():
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
    cafes_list = [cafe.to_dict() for cafe in cafes]
    return render_template('index.html', cafes = cafes_list)

@app.route('/search')
def search():
    search_query = request.args.get('search')
    
    if search_query:
        normalized_query = unidecode(search_query).lower()
        
        # Get all cafes and filter in Python (for accent-insensitive search)
        all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
        cafes = [
            cafe for cafe in all_cafes 
            if normalized_query in unidecode(cafe.name).lower() 
            or normalized_query in unidecode(cafe.location).lower()
        ]
        cafes_list = [cafe.to_dict() for cafe in cafes]
    else:
        cafes_list = []
    
    return render_template('index.html', cafes=cafes_list)

@user_only
@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    if request.method == "POST":
        cafe_name = request.form.get('name')
        map_url = request.form.get('map_url')
        img_url = request.form.get('img_url')
        location = request.form.get('location')
        seats = int(request.form.get('seats'))
        coffee_price = request.form.get('coffee_price')

        has_wifi = bool(request.form.get('has_wifi'))
        has_sockets = bool(request.form.get('has_sockets'))
        has_toilet = bool(request.form.get('has_toilet'))
        can_take_calls = bool(request.form.get('can_take_calls'))
        new_cafe = Cafe(
            name = cafe_name, 
            map_url = map_url,
            img_url = img_url, 
            location = location, 
            seats = seats, 
            coffee_price = coffee_price, 
            has_wifi = has_wifi, 
            has_toilet = has_toilet, 
            can_take_calls = can_take_calls, 
            has_sockets = has_sockets
        )
        try:
            db.session.add(new_cafe)
            db.session.commit()
            return redirect(url_for('home'))  # Redirect to home page on success
        except Exception as e:
            db.session.rollback()  # Rollback the session
            return render_template('add_cafe.html', error="Failed to add cafe. It might already exist.")

    return render_template('add_cafe.html')

@user_only
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_cafe(id):
    cafe = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()
    form = EditForm(
        name = cafe.name,
        map_url = cafe.map_url, 
        img_url = cafe.img_url,
        location = cafe.location, 
        seats = cafe.seats, 
        coffee_price = cafe.coffee_price, 
        has_toilet = cafe.has_toilet, 
        has_wifi = cafe.has_wifi, 
        has_sockets = cafe.has_sockets, 
        can_take_calls = cafe.can_take_calls
    )

    if form.validate_on_submit():
        if form.delete.data:
            db.session.delete(cafe)
            db.session.commit()
            return redirect(url_for('home'))
        elif form.submit.data:
            cafe.name = form.name.data
            cafe.map_url = form.map_url.data
            cafe.img_url = form.img_url.data
            cafe.location = form.location.data
            cafe.seats = form.seats.data
            cafe.coffee_price = form.coffee_price.data
            cafe.has_toilet = form.has_toilet.data
            cafe.has_wifi = form.has_wifi.data
            cafe.has_sockets = form.has_sockets.data
            cafe.can_take_calls = form.can_take_calls.data
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('edit.html', form=form, id=id)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = NewUser()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        plain_password = form.password.data
        if db.session.execute(db.select(User).where(User.email == email)).scalar():
            flash("The user already exist, login instead")
            return redirect(url_for('login'))
        encrypted_password = generate_password_hash(plain_password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(
            username=username, 
            email=email, 
            password=encrypted_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('The email or password dont match. Try again')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/likes/<int:id>')
def press_likes(id):
    current_cafe = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()
    
    if not current_cafe:
        return jsonify({"error": "Cafe not found"}), 404
    
    if current_cafe.likes is None:
        current_cafe.likes = 1
    else:
        current_cafe.likes += 1
    
    db.session.commit()
    return redirect(url_for('home'))  
    

# api operations

@user_only
@app.route('/api', methods=["GET", "POST"])
def use_api():
    form = ApiKeyForm()
    key = session.pop('new_api_key', None)  
    
    if form.validate_on_submit():
        key = secrets.token_urlsafe(32)
        current_user.api_key = key # Store in database
        db.session.commit()
        session['new_api_key'] = key  
        flash("Please Save your API Key after pressing the Generate button. The key will only show one time!")
        return redirect(url_for('use_api'))  # Redirect to prevent resubmission
        
    return render_template('api.html', form=form, key=key)

@app.route('/all', methods=['GET'])
def get_all_cafes():
    api_key = request.headers.get("Authorization")
    
    if not api_key:
        return jsonify({"error": "API key required"}), 401
    
    user = db.session.execute(db.select(User).where(User.api_key == api_key)).scalar()
    
    if not user:
        return jsonify({"error": "Invalid API key"}), 401
    
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
    cafes_list = [cafe.to_dict() for cafe in cafes]
    return jsonify(cafes=cafes_list)

@app.route('/add_cafe', methods=["POST"])
def api_add_cafe():
    api_key = request.headers.get("Authorization")
    if not api_key:
        return jsonify({'error': 'API key is required'}), 401
    
    user = db.session.execute(db.select(User).where(User.api_key == api_key)).scalar()

    if not user:
        return jsonify({'error': 'Api key invalid'}), 401

    new_cafe = Cafe(
            name = request.args.get('cafe_name'), 
            map_url = request.args.get('map_url'),
            img_url = request.args.get('img_url'), 
            location = request.args.get('location'), 
            seats = request.args.get('seats'), 
            coffee_price = request.args.get('coffee_price'), 
            has_wifi = bool(request.args.get('has_wifi')), 
            has_toilet = bool(request.args.get('has_toilet')), 
            can_take_calls = bool(request.args.get('can_take_calls')), 
            has_sockets = bool(request.args.get('has_sockets'))
        )
    
    try:
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify({'success': 'successfully add new cafe in the db'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Some error occur: {e}'}), 400
    
@app.route('/delete/<int:id>', methods=["DELETE"])
def delete(id):
    user_key = request.headers.get("Authorization")
    
    if not user_key:
        return jsonify({'error': 'You need an valid API key to proceed'})

    user = db.session.execute(db.select(User).where(User.api_key == user_key)).scalar()

    if not user:
        return  jsonify({'error': 'You need an valid API key to proceed'})
    
    current_cafe = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()

    if not current_cafe:
        return jsonify({'error': 'Cafe not found'}), 404
    
    if user and current_cafe:
        try:
            db.session.delete(current_cafe)
            db.session.commit()
            return jsonify({'success': 'Cafe deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Some error occur: {e}'}), 400

@app.route('/update_cafe/<int:id>', methods=["PUT", "PATCH"])
def api_update_cafe(id):
    api_key = request.headers.get("Authorization")
    
    if not api_key:
        return jsonify({'error': 'API key is required'}), 401
    
    user = db.session.execute(db.select(User).where(User.api_key == api_key)).scalar()
    if not user:
        return jsonify({'error': 'Invalid API key'}), 401
    
    cafe = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()
    if not cafe:
        return jsonify({'error': 'Cafe not found'}), 404
    
    # Get JSON data from request body
    data = request.json
    
    try:
        # Update only provided fields
        if 'name' in data:
            cafe.name = data['name']
        if 'location' in data:
            cafe.location = data['location']
        if 'map_url' in data:
            cafe.map_url = data['map_url']
        if 'img_url' in data:
            cafe.img_url = data['img_url']
        if 'seats' in data:
            cafe.seats = data['seats']
        if 'coffee_price' in data:
            cafe.coffee_price = data['coffee_price']
        if 'has_wifi' in data:
            cafe.has_wifi = bool(data['has_wifi'])
        if 'has_toilet' in data:
            cafe.has_toilet = bool(data['has_toilet'])
        if 'has_sockets' in data:
            cafe.has_sockets = bool(data['has_sockets'])
        if 'can_take_calls' in data:
            cafe.can_take_calls = bool(data['can_take_calls'])
        
        db.session.commit()
        return jsonify({'success': 'Cafe updated successfully', 'cafe': cafe.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Update failed: {e}'}), 400