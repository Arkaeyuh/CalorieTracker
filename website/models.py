from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    
    meals = relationship('UserMeal', back_populates='user')
    
class FoodItem(db.Model):
    __tablename__ = 'food_items'
    
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    food_name = Column(db.String(100), nullable=False)
    calories = Column(db.Integer, nullable=False)
    protein = Column(db.Float)
    carbs = Column(db.Float)
    fat = Column(db.Float)
    
    meals = relationship('UserMeal', back_populates='food_item')
    
class UserMeal(db.Model):
    __tablename__ = 'user_meals'
    
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = Column(db.Integer, ForeignKey('users.id'))
    food_id = Column(db.Integer, ForeignKey('food_items.id'))
    portion_size = Column(db.Float, nullable=False)
    meal_time = Column(TIMESTAMP, server_default=func.now())
    
    user = relationship('User', back_populates='meals')
    food_item = relationship('FoodItem', back_populates='meals')