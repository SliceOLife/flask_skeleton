#!/usr/bin/env python
from flask import jsonify,send_file, Response, session, redirect, url_for, abort,render_template, g, request
from application import app, db, auth, User


@app.route('/',methods=['GET','POST'])
def index():
  return render_template('templates/index.html')

@app.route('/api/users', methods=['POST'])
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')
	if username is None or password is None:
		abort(400)
	if User.query.filter_by(username=username).first() is not None:
		abort(400)
	user = User(username=username)
	user.hash_password(password)
	db.session.add(user)
	db.session.commit()
	return (jsonify({'username': user.username}), 201,
    	{'Location': url_for('get_user', id=user.id, _external=True)})

@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})
