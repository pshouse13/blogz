from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

#classes
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(200))

    def __init__(self, title, body):
        self.title = title
        self.body = body

#begin handlers
@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

    return render_template('blog.html')

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']
        new_post = Blog(new_title, new_body)
        db.session.add(new_post)
        db.session.commit()
    else:
        return render_template('newpost.html')

#run app
if __name__ == "__main__":
    app.run()