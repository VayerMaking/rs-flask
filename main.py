from flask import Flask
from flask import render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory
import time
from datetime import datetime
import config
import hashlib
import random
import string
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def verify_password(self, password):
        return self.password == hash_password(password)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String, nullable=False)
    title = db.Column(db.String(30), nullable = False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable = False)
    content = db.Column(db.String, nullable = False)
    picture = db.Column(db.String(48), nullable = True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    topic = db.Column(db.String)

def topic_return():
	page = request.args.get('page', 1, type=int)
	return Topic.query.order_by(Topic.timestamp.asc()).paginate(page=page, per_page=25)

def post_return():
	return Post.query.all()

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    if request.method == "GET":
        return render_template('index.html', topics=topic_return())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        data = request.form
        user = User(username=data['username'], password=hash_password(data['password']))
        db.session.add(user)
        db.session.commit()

        return render_template('login.html')
    elif request.method == "GET":

        return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.form
        user = User.query.filter_by(username=data['username'], password=hash_password(data['password'])).first()
        if not user:
            return render_template("login.html", message="invalid credentials")

        session['username'] = data['username']

        return redirect(('/'))

    elif request.method == "GET":
        return render_template("login.html")

@app.route("/topic/", methods=['GET'])
def topic():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.asc()).filter_by(topic=request.args.get('topic')).paginate(page=page, per_page=25)
    return render_template("topic.html", posts=posts, topic=request.args.get('topic'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/new_topic', methods = ['GET', 'POST'])
def new_topic():

	if request.method == "POST":
		data = request.form

		topic = Topic(
			   author = session['username']	,
			   title = data['title'],
			)

		db.session.add(topic)
		db.session.commit()

		return redirect('/')

	else:
		return render_template("create_topic.html")

@app.route('/topic/new_post/', methods = ['GET', 'POST'])
def new_post():

    if request.method == "POST":
        data = request.form

        file = request.files['post_image']

        if file and file.filename != '' and allowed_file(file.filename):
            file.filename = random_string(48)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        post = Post(
            author = session['username'],
            title = data['post_title'],
            content = data['post_content'],
            picture = file.filename,
            topic = request.args.get('topic')
			)

        db.session.add(post)
        db.session.commit()

        return redirect('/')

    else:
        return render_template("create_post.html", topic=request.args.get('topic'))

@app.route('/post/', methods = ['GET', 'POST'])
def post():
	post = Post.query.filter_by(title=request.args.get('post_title')).first()
	return render_template("post.html", post=post)

@app.route('/post/update_post/', methods = ['GET', 'POST'])
def update_post():
    if request.method == "POST":
        data = request.form

        file = request.files['post_image']

        if file and file.filename != '' and allowed_file(file.filename):
            file.filename = random_string(48)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        post = Post.query.filter_by(title=request.args.get('post_title')).first()
        post.title = data['post_title']
        post.content = data['post_content']
        if file.filename:
            post.picture = file.filename

        db.session.commit()

        return redirect('/')

    else:
        post = Post.query.filter_by(title=request.args.get('post_title')).first()
        if post.author == session['username']:
            return render_template("update_post.html", author=post.author)
        else:
            return render_template('forbidden_update.html')

@app.route('/post/delete_post/', methods = ['GET', 'POST'])
def delete_post():
    post = Post.query.filter_by(title=request.args.get('post_title')).first()
    if post.author == session['username']:
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('forbidden_delete.html')

@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    directory = os.path.join('..', app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory, filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for x in range(length))

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
