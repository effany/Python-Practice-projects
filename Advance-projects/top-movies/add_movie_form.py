from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

class AddMoiveForm(FlaskForm):
    movie_title = StringField("Add a movie")
    submit = SubmitField("Add")
