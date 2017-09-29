#!/usr/bin/env python

from flask import Flask, request, jsonify
app = Flask(__name__)

languages =[{'name':'Javascript'}, {'name':'Python'}, {'name':'Ruby'}, {'name':'Django'}]
@app.route("/", methods=['GET'])
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
	neme = request.json['name']
	language = {'name': request.json['name']}  #{"name":"C++"}
	languages.append(language)
	return jsonify({'languages' : languages})

if __name__ == '__main__':
    app.run(debug=False, port=8080)

