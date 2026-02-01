from flask import Flask, render_template, jsonify, request, redirect, flash, abort, session, url_for
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_bootstrap import Bootstrap5
from forms import RegisterForm, LoginForm, ShippingForm
from payment_manager import PaymentManager
import os
from dotenv import load_dotenv
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from cart_manager import CartManger
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import random
import uuid
import json
import stripe
from unidecode import unidecode

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('flask_secret_key')


class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item.db'
login_manager = LoginManager()
payment_manager = PaymentManager()
login_manager.init_app(app)
db = SQLAlchemy(model_class=Base)
db.init_app(app)
bootstrap = Bootstrap5(app)

cart_manager = CartManger()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class Item(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    image_url: Mapped[str] = mapped_column(String(250), nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    on_discount: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    discount_price: Mapped[float] = mapped_column(nullable=True)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now()) 

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    orders: Mapped[list["Orders"]] = relationship(back_populates='user')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class Orders(db.Model):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_number: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates='orders')
    items: Mapped[str] = mapped_column(String, nullable=False)  # Store as JSON string
    total_amount: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(50), default='pending', nullable=False)
    shipping_address: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    page = db.paginate(db.select(Item).order_by(Item.id), per_page=12)
    return render_template('index.html', pagination=page)


@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    raw_items_data = request.json
    print(raw_items_data)
    current_cart_items = cart_manager.cart_items

    if len(current_cart_items) != 0:
        found = False  # Track if we found the item
        for existing_item in current_cart_items:
            if raw_items_data['itemSku'] == existing_item['itemSku']:
                existing_item['itemCount'] += 1
                found = True
                break  
        
        if not found:  
            cart_manager.add_item(raw_items_data)
    else:
            cart_manager.add_item(raw_items_data)

    return jsonify({'success': True, 'cart_count': len(cart_manager.cart_items)})


@app.route('/remove-from-cart', methods=['POST'])
@login_required
def remove_from_cart():
    raw_items_data = request.json
    cart_items = cart_manager.cart_items

    for item in cart_items:
        if item['itemSku'] == raw_items_data['itemSku']:
            if item['itemCount'] >= 2:
                item['itemCount'] -= 1
            else:
                cart_items.remove(item)
            
            print(cart_items)
            return jsonify({'success': True, 'cart_count': len(cart_manager.cart_items)})
    
    # Only reach here if item not found
    return jsonify({'success': False, 'message': 'There is no such item in the cart'})
    

@app.route('/cart')
@login_required
def cart():
    cart_items = cart_manager.cart_items
    
    cart_manager.sub_total()
    sub_total = cart_manager.total_price
    return render_template('cart.html', cart_items = cart_items, total_price=sub_total)

@app.route('/login', methods=["POST", "GET"])
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
            flash('The email or password do not match. Try again!')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        entered_email = form.email.data
        password = form.password.data
        name = form.name.data

        if db.session.execute(db.select(User).where(User.email == entered_email)).scalar():
            flash('The user already exist! Login instead')
            return redirect(url_for('login'))

        encrypted_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        new_user = User (
            email = entered_email, 
            password = encrypted_password, 
            name = name, 
            orders = [],
            
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/checkout')
@login_required
def checkout():
    cart_items = cart_manager.cart_items
    order_num = f"ORD-{uuid.uuid4().hex[:12].upper()}"
    

    total_price = 0
    if len(cart_items) > 0:
        
        for item in cart_items:
            item_price = float(item['itemDiscountPrice']) if item['itemDiscountPrice'] != 'None' else float(item['itemPrice'])
            total_price += item_price * item['itemCount']
        
        total_price *= 1.08 

        new_order = Orders (
            user_id = current_user.id, 
            items = json.dumps(cart_items),
            total_amount  = total_price,
            order_number = order_num, 
            shipping_address="",
            status = 'pending'
        )
        db.session.add(new_order)
        db.session.commit()

        #redirect_response = payment_manager.create_session(cart_items, order_num)
        cart_manager.cart_items.clear()
        
        #return redirect_response
        return redirect(url_for('gather_shipping_data', order_num=order_num))
    else:
        flash('There is no item in the cart. Add something in :) ')
        return redirect(url_for('home'))

@app.route('/orders')
@login_required
def orders():
    all_orders = db.session.execute(db.select(Orders).where(Orders.user_id == current_user.id).order_by(Orders.created_at.desc())).scalars().all()
    # Parse JSON items for each order
    for order in all_orders:
        order.parsed_items = json.loads(order.items)
    return render_template('orders.html', all_orders=all_orders)

@app.route('/success')
@login_required
def success_payment():
    session_id = request.args.get('session_id')
    
    if session_id:
        stripe_session = payment_manager.retrieve_payment_status(session_id)
        
        # Update order status if payment is complete
        if stripe_session.payment_status == 'paid':
            order_num = stripe_session.metadata.get('order_number')
            order = db.session.execute(
                db.select(Orders).where(Orders.order_number == order_num)
            ).scalar()
            
            if order:
                order.status = 'paid'
                db.session.commit()
                
        return render_template('success_payment.html', 
                             payment_status=stripe_session.payment_status,
                             order_number=stripe_session.metadata.get('order_number'))
    
    return render_template('success_payment.html')


@app.route('/latePayments/<orderNum>')
def late_payment(orderNum):
        order_data = db.session.execute(db.select(Orders).where(Orders.order_number == orderNum)).scalar()
        cart_items = json.loads(order_data.items)
        payment_session = payment_manager.create_session(cart_items, orderNum)
        return payment_session

@app.route('/cancel_order/<orderNum>')
def cancel_order(orderNum):
    order_data = db.session.execute(db.select(Orders).where(Orders.order_number == orderNum)).scalar()
    db.session.execute(
        db.update(Orders).where(Orders.order_number == orderNum)
        .values(status="cancel")
    )
    db.session.commit()
    return redirect(url_for('orders'))

@app.route('/shipping', methods=['GET', 'POST'])
def gather_shipping_data():
    order_num = request.args.get('order_num')
    shippingForm = ShippingForm()

    if shippingForm.validate_on_submit():
        country = (shippingForm.country.data).lower()
        city = (shippingForm.city.data).lower()
        post_code = shippingForm.post_code.data
        address = (shippingForm.shipping_address.data).lower()

        full_address = str(post_code) + country + city + address
        db.session.execute(
            db.update(Orders)
            .where(Orders.order_number == order_num)
            .values(shipping_address=full_address)
        )
        db.session.commit()
        return redirect(url_for('late_payment', orderNum=order_num))

    return render_template('shipping.html', shippingForm=shippingForm, order_num=order_num)

@app.route('/search', methods=["GET"])
def search():
    search_query = request.args.get('search')
    if search_query:
        normalized_query = unidecode(search_query).lower()
        # Get all items (without pagination for search)
        all_items = db.session.execute(db.select(Item)).scalars().all()
        filtered_items = [
            item for item in all_items
            if normalized_query in unidecode(item.name).lower()
            or normalized_query in unidecode(item.description).lower()
        ]
        
        # Create a simple object that mimics pagination for the template
        class SearchResults:
            def __init__(self, items):
                self.items = items
                self.prev_num = None
                self.next_num = None
            
            def iter_pages(self):
                return []  # No pagination for search results
        
        pagination = SearchResults(filtered_items)
    else:
        # If no search query, show all items with pagination
        pagination = db.paginate(db.select(Item).order_by(Item.id), per_page=12)
        
    return render_template('index.html', pagination=pagination)
