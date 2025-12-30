from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField

class EditForm(FlaskForm):
    rating = FloatField('Your Rating our of 10. ex. 7.5')
    review = StringField("Your Review")
    submit = SubmitField("Done")
