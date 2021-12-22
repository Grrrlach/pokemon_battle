from flask import Flask, render_template, request
from config import Config
from flask_login import LoginManager #for logging users in and maintaining a session
from flask_sqlalchemy import SQLAlchemy #this talk to our database for us
from flask_migrate import Migrate #Makes altering the Database a lot easier
from flask_moment import Moment


# init Login Manager
login = LoginManager()
#where to be sent if you are not logged in
#there are settings in LoginManager. \
# login_view is one.
login.login_view = 'auth.login'
# init the database from_object
db = SQLAlchemy()
# init Migrate. tells the app how to make changes\
#  to db without breaking anything
#could be in models, should be, and imported to here
migrate = Migrate()

moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    #register our plugins
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    #Register our blueprints with the app
    #local import is solution, otherwise it becomes circular import
    from . blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from . blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.social import bp as social_bp
    app.register_blueprint(social_bp)

    from .blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)
    
    return app