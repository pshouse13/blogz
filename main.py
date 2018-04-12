from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(200))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    blog_entry = Blog.query.filter_by(body=body).first()
    return render_template('blog.html')

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        title = request.form['title']
        entry = request.form['entry']

        #validate info

        blog = Blog.query.filter_by(entry=entry).first()
        if not blog:
            new_blog = Blog(title, entry)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog')
        else:
            return '<h1> Add an entry </h1>'

    return render_template('newpost.html')
