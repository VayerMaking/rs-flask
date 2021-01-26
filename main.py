from flask import Flask
from flask import render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime
import config
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
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
    author = db.Column(db.String)
    title = db.Column(db.String(30), nullable = False)
    content = db.Column(db.String, nullable = False)
    posts = []

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String)
    content = db.Column(db.String, nullable = False)
    picture = db.Column(db.String(48), nullable = True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def topic_return():
	return set(Topic.query.all())

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():

	if request.method == "GET":
	    if 'username' in session:
	        username = session['username']
	        
	        return render_template('index.html', username=username, topics=topic_return())

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
            return render_template("index.html")

        session['username'] = data['username']

        return redirect(('/'))
        
    elif request.method == "GET":
        return render_template("login.html")

@app.route("//<string:topic>")
def homepage(topic):
    #val = request.args.get('hello')
    # get the name, text,image based on the topic(query_string)
    return render_template("topic.html", topic=topic)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/new_topic', methods = ['GET', 'POST'])
def new_topic():

	if request.method == "POST": 
		data = request.form
		
		topic = Topic(
			   author = session['username']	,	
			   title = data['title'],
			   content = data['content'],
			)
		
		db.session.add(topic)
		db.session.commit()
		
		return redirect('/')
	
	else:
		return render_template("create_topic.html")


if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
	
