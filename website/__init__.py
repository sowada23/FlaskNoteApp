from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy() #Initialize SQLAlchemy instance
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__) 
    app.config['SECRET_KEY'] = 'soraowada' # Set secret key for session management
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # Set the database URI for SQLAlachem
    db.init_app(app) #Initialize the app with SQLAlchemy

    from .views import views # Import views blueprint from views module which is views.py
    from .auth import auth # Import auth blueprint from auth module which is auth.py

    app.register_blueprint(views, url_prefix='/') # Registering views blueprint means that the routes defined in the views blueprint 
    app.register_blueprint(auth, url_prefix='/')     

    from .models import User, Note # Import models to ensure they are registered with SQLAlchemy

    with app.app_context():
        db.create_all()

    login_manager = LoginManager() # Initializes the login manager
    login_manager.login_view = 'auth.login' # Sets the login view for the login manager
    login_manager.init_app(app) # Initializes the login manager with app
    login_manager.login_message = None
    
    @login_manager.user_loader # It tells Flask-Login that the function load_user will be used to load a user from the user ID stored in the session.
    def load_user(id): # This function queries the database for a user with the given ID and returns User object
        return User.query.get(int(id))

    return app

def create_database(app): # This function is used to create database tables
    with app.app_context():
        if not path.exists('website/' + DB_NAME): # Check if the database file exists # Creates the database tables if the file does not exist.
            db.create_all()
            print('Created Database!')
