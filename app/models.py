from app import db
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
import requests


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(200), unique=True, index=True)
    password = db.Column(db.String(200))
    icon = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.icon = data['icon']
        self.password = self.hash_password(data['password'])

    #salts and hashes password
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    #compares the user password to the password provided
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    #saving the user to the database
    def save(self):
        db.session.add(self) #adding user to the db session
        db.session.commit() #saving the change to the db session
    
    def get_icon_url(self):
        url= f'https://pokeapi.co/api/v2/pokemon/{self.icon}'
        response = requests.get (url)
        info = response.json()
        sprite_location=info ['sprites']['front_shiny']
        return sprite_location

@login.user_loader
def load_user(id):
    return User.query.get(int(id)) #.get only works for primary keys, returns whole row
    #like saying SELECT * FROM user WHERE id = x