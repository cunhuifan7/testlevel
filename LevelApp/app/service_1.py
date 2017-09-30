#!/usr/bin/env python

import pymysql.cursors
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://testlevel:xiaoshen@localhost/testleveldb'
db = SQLAlchemy(app)

def mysql_query():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='testlevel',
                                 password='xiaoshen',
                                 db='testleveldb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            #sql = "INSERT INTO 'user' ( 'username', 'email') VALUES (%s, %s)"
            #cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
            sql = "INSERT INTO `user` (`username`, `email`) VALUES (%s, %s)"
            cursor.execute(sql, ('very-secret5', 'webmaster@python.org5'))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            #sql = "SELECT 'id', 'username' , 'email' FROM 'user' WHERE 'email'=%s"
            sql = "SELECT `id`, `username`, `email` FROM `user` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()

###!/bin/user/python

#from flask import Flask



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
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/post/<int:post_id>")
def post(post_id):
    user=User.query.filter_by(id=post_id).one()
    userAll = User.query.all()
    return render_template('post.html', post=user, userAll=userAll)


@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
    username = request.form['username']
    email = request.form['email']
    newuser = User(username, email)
    db.session.add(newuser)
    db.session.commit()
    return redirect(url_for('index')) #render_template('post.html')

languages =[{'name':'Javascript'}, {'name':'Python'}, {'name':'Ruby'}, {'name':'Django'},{'name':'C#'}]
@app.route("/t", methods=['GET'])
def test():
    return jsonify({'message':'It works!'})

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/search/')
#@app.route("/search1", methods=['GET'])
def search():
    return render_template('search.html')

@app.route('/search1')
#@app.route("/search1", methods=['GET'])
def search1():
    #return render_template('search.html')
     try:
         proglang = request.args.get('proglang')

         langs = [language for language in languages if str(language['name']).lower() == str(proglang).lower()]
         if len(langs) > 0:
            return jsonify(result=langs[0])
         else:
            return jsonify(result='Try again')
     except Exception, e:
         #return(str(e))
         return render_template('search.html')


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


# @app.route("/homecontrol/api/v1.0/temperature", methods=['POST'])
# def api_temperature():
#     if request.headers['Content-Type'] == 'text/plain':
#         print (request.data)
#         return 'OK', 200
#     elif request.headers['Content-Type'] == 'application/json':
#         print (json.dumps(request.json))
#         mongo_client['HomeControl']['temperature'].insert(request.json)
#         print (mongo_client['HomeControl']['temperature'].count ())
#         return "OK", 200
#     else:
#         return "Unsupported Media Type", 415


if __name__ == "__main__":
    app.run()
