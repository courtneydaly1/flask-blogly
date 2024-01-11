"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = 'https://unsplash.com/photos/black-framed-sunglasses-on-white-surface-lSl94SZHRgA'

 
def connect_db(app):
    """connect database to this flask app"""
        
    db.app = app
    db.init_app(app)

class User(db.Model):
    """creates new user"""
    
    __tablename__= 'users'    
    
    id = db.Column(db.Integer, primary_key= True)
    first_name = db.Column(db.Text, nullable= False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = DEFAULT_IMAGE_URL)
    
   
    