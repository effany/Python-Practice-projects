from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class ShippingForm(FlaskForm):
    country = StringField("Your shipping country", validators=[DataRequired()])
    city = StringField("Your city", validators=[DataRequired()])
    post_code = IntegerField("Your postcode", validators=[DataRequired()])
    shipping_address = StringField("enter your address", validators=[DataRequired()])
    submit = SubmitField("Let's go!")
