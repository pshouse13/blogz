from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from app import app, db 
from models import Blog, User
from hashutils import make_pw_hash, check_pw_hash


def logged_in_user():
    owner = User.query.filter_by(username=session['username']).first()
    return owner

endpoints_without_login = ['login', 'register', 'index', 'blog']

@app.before_request
def require_login():
    if not ('username' in session or request.endpoint in endpoints_without_login):
        return redirect("/login")

@app.route('/')
def index():

    users = User.query.all()
    
    return render_template('index.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        if users.count() == 1:
            user = users.first()
            if user and check_pw_hash(password, user.pw_hash):
                session['username'] = user.username
                flash('Welcome back, '+user.username)
                return redirect("/")
        flash('Bad username or password')
        return redirect("/login")

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        username_db_count = User.query.filter_by(username=username).count()
        if username_db_count > 0:
            flash('Oh, no! ' + username +  ' is already taken!')
            return redirect('/signup')
        if password != verify:
            flash('Passwords did not match')
            return redirect('/signup')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        return redirect("/")
    else:
        return render_template('signup.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    blog_id = request.args.get('id')
    user_id = request.args.get('userid')
    posts = Blog.query.all()

    if blog_id:
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template("solo.html", title=post.title, body=post.body, user=post.owner.username, user_id=post.owner_id)
    if user_id:
        entries = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('singleUser.html', entries=entries)

    return render_template('blog.html', posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_entry = Blog(title, body, owner)

        if new_entry.validate_entry():
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/blog?id=' + str(new_entry.id))
        else:
            flash("Please do not leave either form blank.")
            return render_template('newpost.html', title=title, body=body, owner=owner)
    else:
        return render_template('newpost.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

#run app
if __name__ == "__main__":
    app.run()