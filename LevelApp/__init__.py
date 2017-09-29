#!/usr/bin/env python

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

###!/bin/user/python

#from flask import Flask


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://testlevel:xiaoshen@localhost/testleveldb'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

#admin = User('admin', 'admin@example.com')

#db.create_all() # In case user table doesn't exists already. Else remove it.    

#db.session.add(admin)

#db.session.commit() # This is needed to write the changes to database

user_all = User.query.all()

user_admin = User.query.filter_by(username='admin').first()

@app.route("/")
def index():
    return "Hello, I love Digital Ocean!"


languages =[{'name':'Javascript'}, {'name':'Python'}, {'name':'Ruby'}, {'name':'Django'}]
@app.route("/t", methods=['GET'])
def test():
    return jsonify({'message':'It works!'})

@app.route('/lang', methods=['GET'])
def returnAll(): 
    return jsonify({'languages':languages})

@app.route('/lang/<string:name>', methods=['GET'])
def returnOne(name):
	langs = [language for language in languages if language['name'] == name]
	return jsonify({'language':langs[0]})

@app.route('/lang', methods=['POST'])
def addOne():
	neme = request.get_json(force=True) #get_json(force=True)
	language = {'name': neme}  #{"name":"C++"}
	languages.append(language)
	return jsonify({'languages' : languages})


if __name__ == "__main__":
    app.run()

