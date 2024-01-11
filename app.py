"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY']= 'shhSecret!'

toolbar = DebugToolbarExtension(app)

app.app_context().push()
app.run(debug=True)


connect_db(app)
db.create_all()

@app.route('/')
def redirect_page():
    """redirects home page to user's page"""
    return redirect('/users')

@app.route('/users')
def user_homepage():
    """Show the page with all the users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)    

@app.route('/users/new', methods= ['GET'])
def new_user_form():
    """show a form to create a new user"""
    return render_template('/users/new.html')

@app.route('/users/new', methods= ['POST'])
def handle_new_user():
    """handle form for new users"""
    
    new_user= User(
        first_name= request.form['first_name'],
        last_name= request.form['last_name'],
        image_url= request.form['image_url'] or None
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_info(user_id):
    """Show info about the user"""
    
    user= User.query.get_or_404(user_id)
    return render_template('/users/show.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET'])
def edit_user(user_id):
    """uses a form to edit current users"""
    
    user= User.query.get_or_404(user_id)
    return render_template('/users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """handle form to update current user"""
    
    user= User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """handles the form to delete current user"""
    
    user= User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')
    
