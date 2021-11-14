from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


# class flask_wtf.Form()

class PokemonForm(FlaskForm):
    poke_id = StringField('Search for a Pokemon', validators = [DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')