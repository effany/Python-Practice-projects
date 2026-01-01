from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config["UPLOAD_FOLDER"] = "static/files"
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=60)
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        plain_password = request.form["password"]
        entered_email = request.form["email"]
        entered_name = request.form["name"]

        if db.session.execute(db.select(User).where(User.email == request.form["email"])).scalar():
            flash("The user already exist! Login instead")
            return render_template("login.html")
        
        encrpyted_pass = generate_password_hash(plain_password, method="pbkdf2:sha256", salt_length=8 )
        new_user = User(
            email = entered_email,
            name = entered_name, 
            password = encrpyted_pass
        )
        
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return render_template("secrets.html", name = request.form["name"])
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('secrets'))
        else:
            flash("Invalid email or password")
    return render_template("login.html")

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download/<path:name>')
@login_required
def download(name):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"], name, as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)
