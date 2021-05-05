from flask import Flask , request, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm, EditFeedback


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'kakakaka'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def redirect_to_register():
    return redirect('/register')

@app.route('/register', methods = ['GET','POST'])
def register_user():

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data 
        email = form.email.data 
        password = form.password.data 
        first_name = form.first_name.data 
        last_name = form.last_name.data
        new_user = User.register(username,email,password,first_name,last_name)
        session['user_id'] = new_user.username
        db.session.add(new_user)
        db.session.commit()
        return redirect(f'/users/{new_user.username}')
    else:

        return render_template('register.html', form = form)
    

@app.route('/login', methods = ['GET','POST'])
def login_user():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session['user_id'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form = form)

@app.route('/users/<username>')
def get_users(username):
    user = User.query.get_or_404(username)
    feedbacks = Feedback.query.all()
    if "user_id" not in session:
        flash ('Please login first')
        return redirect('/login')
    else:
        return render_template('users.html' , user=user, feedbacks = feedbacks)

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods =['GET','POST'])
def add_feedback(username):
    user = User.query.get_or_404(username)
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title = title, content = content, user_username = user.username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{user.username}')
    if "user_id" not in session:
        flash ('Please login first')
        return redirect('/login')
    else:
        return render_template('add_feedback.html' , user=user, form = form)
    
        
        
@app.route('/feedback/<feedback_id>/edit', methods =['GET','POST'])
def edit_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    user = User.query.get_or_404(feedback.user_username)
    
    form = EditFeedback()
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
       
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{user.username}')
    if "user_id" not in session:
        flash ('Please login first')
        return redirect('/login')
    else:
        return render_template('edit_feedback.html' , user=user, form = form)
    
    
    
@app.route('/feedback/<feedback_id>/delete', methods =['GET','POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{feedback.user_username}')



@app.route('/users/<username>/delete', methods =['GET','POST'])
def delete_user(username):
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

