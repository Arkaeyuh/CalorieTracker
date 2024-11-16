from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv, find_dotenv
import os

db = SQLAlchemy()
DB_NAME = "database.db"

load_dotenv()

def create_app():
    app = Flask(__name__)
    SECRET_KEY = os.getenv('SECRET_KEY')
    FOODDATA_API_KEY = os.getenv('FOODDATA_API_KEY')
    app.config['SECRET_KEY'] = SECRET_KEY
    # print(SECRET_KEY)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['FOODDATA_API_KEY'] = FOODDATA_API_KEY
    # print(FOODDATA_API_KEY)
    db.init_app(app)
    
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, FoodItem, UserMeal
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    with app.app_context():
        db.create_all()
    
    return app

