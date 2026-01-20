from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, URLField
from wtforms.validators import DataRequired, Email, URL, Optional

class NewUser(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Log in") 

class ApiKeyForm(FlaskForm):
    generate = SubmitField("Generate")

class EditForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = URLField('Map URL', validators=[DataRequired(), URL()])
    img_url = URLField('Image URL', validators=[Optional(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    seats = StringField('Seats (e.g., 20-30)', validators=[Optional()])
    coffee_price = StringField('Coffee Price (e.g., 2.50)', validators=[Optional()])
    has_toilet = BooleanField('Has Toilet')
    has_wifi = BooleanField('Has WiFi')
    has_sockets = BooleanField('Has Power Sockets')
    can_take_calls = BooleanField('Can Take Calls')
    submit = SubmitField('Update Cafe')



