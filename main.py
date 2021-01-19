from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#from active_alchemy import ActiveAlchemy
import time
from datetime import datetime
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        data = request.form
        user = User(username=data['username'], password=data['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('register'))
        return render_template('register.html')
    elif request.method == "GET":
        #user = User.query.first()
        return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.form
        user = User(username=data['username'], password=data['password'])
        return redirect(url_for('login'))
        return render_template('login.html')
    elif request.method == "GET":
        return render_template("login.html")


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
