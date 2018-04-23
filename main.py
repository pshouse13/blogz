from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from app import app, db 
from models import Blog, User
from hashutils import make_pw_hash, check_pw_hash


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index'] #fix so blog and index work without login
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():

    users = User.query.all()

    singleUser = request.args.get('user.id') #figure this out
    

    return render_template('index.html', users=users)

@app.route('/login', methods=['POST', 'GET'])
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
                session['user'] = user.username
                flash('Welcome back, '+user.username)
                return redirect("/")
        flash('Bad username or password')
        return redirect("/login")

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate info 

        user = User.query.filter_by(username=username).first()
        if not user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('Username already in use' or 'Passwords do not match')

    return render_template('signup.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    blogs = Blog.query.all()

    blog_id = request.args.get('id')
    if (blog_id):
        blog = Blog.query.get(blog_id)
        return render_template('solo.html', blog=blog)

    singleUser = request.args.get('userid')
    if (singleUser):
        post = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('singleUser.html', post=post)
    
    return render_template('blog.html', blogs=blogs)

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

#run app
if __name__ == "__main__":
    app.run()