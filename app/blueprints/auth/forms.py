from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.fields.core import RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
import random
from jinja2 import Markup
import requests



class LoginForm(FlaskForm):
    email = StringField('Email Address', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enter, Pokemon Trainer. Pokeknowledge awaits!')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(), EqualTo('confirm_password', message="Your passwords didn't match!")])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password', message="Your passwords didn't match!")])
    submit = SubmitField('Register, brave Pokemon Trainer!')
    


# url = f"https://pokeapi.co/api/v2/pokemon/{r1}"
# response = requests.get (url)
# data = response.json()       
# poke_dict={
#     'poke_name': data ['forms'][0] ['name'],
#     'hp_base': data ['stats'][0] ['base_stat'],
#     'attack_base': data ['stats'][1] ['base_stat'],
#     'defense_base': data ['stats'][2] ['base_stat'],
#     'front_shiny_sprite': data ['sprites']['front_shiny']
#     }



    r1=random.randint(1,225)
    r2=random.randint(226,450)
    r3=random.randint(451,675)
    r4=random.randint(676,898)


# https://pokeapi.co/api/v2/pokemon/{poke_id}

    url = f"https://pokeapi.co/api/v2/pokemon/{r1}"
    response = requests.get (url)
    info = response.json()
    sprite_location=info ['sprites']['front_shiny']
    r1_img=Markup(f'<img src="{sprite_location}", style="height:75px">')

    url = f"https://pokeapi.co/api/v2/pokemon/{r2}"
    response = requests.get (url)
    info = response.json()
    sprite_location=info ['sprites']['front_shiny']
    r2_img=Markup(f'<img src="{sprite_location}", style="height:75px">')

    url = f"https://pokeapi.co/api/v2/pokemon/{r3}"
    response = requests.get (url)
    info = response.json()
    sprite_location=info ['sprites']['front_shiny']
    r3_img=Markup(f'<img src="{sprite_location}", style="height:75px">')

    url = f"https://pokeapi.co/api/v2/pokemon/{r4}"
    response = requests.get (url)
    info = response.json()
    sprite_location=info ['sprites']['front_shiny']
    r4_img=Markup(f'<img src="{sprite_location}", style="height:75px">')




    icon = RadioField("Choose a pokemon to accompany you while you're here:", 
            choices=[(r1, r1_img),(r2, r2_img),(r3, r3_img),(r4, r4_img)], 
            validators=[DataRequired()])

    
    
    
        #NAME OF DEF MUST BE LIKE THIS: validate_email(). FIELD NAME PRECEDED BY "VALIDATE"
    # def validate_email(form, field):
    #     sr = User.query.filter_by(email = field.data).first() #says to give only first result
    def validate_email(form, field): #could be 'self' and field.
        same_email_user = User.query.filter_by(email = field.data).first() #says to give only first result
        #   Like SELECT * FROM user WHERE email = x
        # filter_by will always return a list, even of 1 user
        #.first says to give only 1 user object, instead of a list. 1 row.
        if same_email_user: 
            #will return None if nobody in database. this is for if it doesn't return None
            raise ValidationError ("We already have a Pokemon trainer using that account!")

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(), EqualTo('confirm_password', message="Your passwords didn't match!")])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password', message="Your passwords didn't match!")])
    submit = SubmitField('Register, brave Pokemon Trainer!')
    
    r1=random.randint(1,225)
    r2=random.randint(226,450)
    r3=random.randint(451,675)
    r4=random.randint(676,898)

    url = f"https://pokeapi.co/api/v2/pokemon/{r1}"
    response = requests.get (url)
    info = response.json()
    sprite_location=info ['sprites']['front_shiny']
    r1_img=Markup(f'<img src="{sprite_location}", style="height:75px">')

    url = f"https://pokeapi.co/api/v2/pokemon/{r2}"
    response = requests.get (url)
    info = response.json()
    sprite_location=info ['sprites']['front_shiny']
    r2_img=Markup(f'<img src="{sprite_location}", style="height:75px">')

    url = f"https://pokeapi.co/api/v2/pokemon/{r3}"
    response = requests.get (url)
    info = response.json()
    sprite_location=info ['sprites']['front_shiny']
    r3_img=Markup(f'<img src="{sprite_location}", style="height:75px">')

    url = f"https://pokeapi.co/api/v2/pokemon/{r4}"
    response = requests.get (url)
    info = response.json()
    sprite_location=info ['sprites']['front_shiny']
    r4_img=Markup(f'<img src="{sprite_location}", style="height:75px">')

    icon = RadioField("Choose a pokemon to accompany you while you're here:", 
            choices=[(10000, "Keep current pokemon"),(r1, r1_img),(r2, r2_img),(r3, r3_img),(r4, r4_img)], 
            validators=[DataRequired()])

#delete this because we added teh edit profile form, and
#don't want to error out the current user's email address
    # def validate_email(form, field): #could be 'self' and field.
    #     same_email_user = User.query.filter_by(email = field.data).first() #says to give only first result

    #     if same_email_user: 
    #         raise ValidationError ("We already have a Pokemon trainer using that account!")

    # def pw_check (confirm_password):
    #     if not confirm_password :
    #         raise ValidationError ("Those passwords do not match!")


