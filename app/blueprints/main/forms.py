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

class BattleForm(FlaskForm):
    my_pokemon_id = StringField("What is the ID of the pokemon you'll be using to battle?", validators= [DataRequired()])
    their_pokemon_id = StringField("What is the ID of the pokemon you wish you challenge?", validators= [DataRequired()])
    submit = SubmitField ("Let's BATTLE!")