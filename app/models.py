from app import db
from flask_login import UserMixin
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
import requests
import secrets

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(200), unique=True, index=True)
    password = db.Column(db.String(200))
    icon = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User', 
        secondary = followers, 
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
        )
    wins = db.Column(db.Integer, default = 0)
    losses = db.Column(db.Integer, default = 0)
    
    token = db.Column(db.String, index = True, unique=True)
    token_exp = db.Column (db.DateTime)

    ########################################################################
    ###########  METHODS FOR TOKEN AUTH ####################################
    ########################################################################
    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        #give the user their existing token in not exp.
        if self.token and self.token_exp > current_time + timedelta(seconds=60):
            return self.token
        #if expired or not exisitng, create new token and exp.
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    def revoke_token (self):
        self.token_exp = dt.utcnow() - timedelta(seconds = 61)
    
    @staticmethod
    def check_token (token):
        u = User.query.filter_by(token = token).first()
        if not u or u.token_exp < dt.utcnow():
            return None
        return u

    ########################################################################
    ############  END METHODS FOR TOKENS  ##################################
    ########################################################################







    #check if user is following someone
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    #follow a user
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()

    #unfollow a user
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()


    #get all the posts from the users I am following
    def followed_posts(self):
        #get all posts for all users I'm is_following
        followed = Post.query.join(
            followers, Post.user_id == 
            followers.c.followed_id).filter(
            followers.c.follower_id == self.id
            )
        #get all my own posts
        self_posts = Post.query.filter_by(user_id = self.id)
        #add together my posts and posts of users I'm following
        all_posts = followed.union(self.posts).order_by(Post.date_created.desc())
        
        return all_posts

        #get all my onw posts

        #add those together

        #sort by date, descending order

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


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=dt.utcnow())
    date_updated = db.Column(db.DateTime, onupdate=dt.utcnow())
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    def save(self):
        db.session.add(self) #copied from the save function above
        db.session.commit()
    
    def edit(self, new_body):
        self.body=new_body
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<id:{self.id} | Post: {self.body[:15]}>'


# !!!!Catcing/Releasing Pokemon
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poke_name = db.Column(db.String(150))
    hit_points = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    image = db.Column(db.String(150))
    move = db.Column (db.String(150))
    move_text = db.Column (db.String(250))
    move_description = db.Column (db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def to_dict(self):
        data={
            'id':self.id,
            'poke_name':self.poke_name,
            'hit_points':self.hit_points,
            'attack':self.attack,
            'defense':self.defense,
            'image':self.image,
            'move': self.move,
            'move_description': self.move_description,
        }
        return data


    def capture(self):
        db.session.add(self)
        db.session.commit()

    def release(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<ID: {self.id} | Body: {self.poke_name}>'

