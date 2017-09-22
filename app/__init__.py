#!/usr/bin/env python

import os

from flask import Flask, request, g, redirect, jsonify, make_response,\
	send_file, after_this_request
from flask_cors import CORS

from config import config
from db.db import SS
import db.model as m
from db import database as db
from .auth import MyAuthMiddleWare


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	db.init_app(app)

	CORS(app, resources={'/api/1.0/*': {'origins': '*'}})

	app.wsgi_app = MyAuthMiddleWare(app.wsgi_app,
		app.config['AUTHENTICATION_LOGIN_URL'],
		public_prefixes=[
			'/static/',
			'/favicon.ico',
			'/health-check',
			'/logout'],
		json_prefixes=['/api/', '/whoami'],
	)

	from app.api import api_1_0
	app.register_blueprint(api_1_0, url_prefix='/api/1.0/')

	@app.before_request
	def set_current_user():
		data = request.environ.get('myauthmiddleware', None)
		userId = int(data['REMOTE_USER_ID'])
		g.current_user = m.User.query.get(699)

	# @app.teardown_request
	# def terminate_transaction(exception):
	# 	if exception is None:
	# 		SS.commit()
	# 	else:
	# 		SS.rollback()
	# 	SS.remove()

	# @app.errorhandler(404)
	# def default_hander(exc):
	# 	if request.path.startswith('/static'):
	# 		return make_response(
	# 			_('Sorry, the resource you have requested for is not found'),
	# 			404)
	# 	if request.path.startswith('/api/'):
	# 		return make_response(jsonify(error='requested url not found'),
	# 			404, {})
	# 	# TODO: only redirect valid urls
	# 	return redirect('/#%s' % request.path)

	@app.route('/whoami')
	def who_am_i():
		me = g.current_user
		resp = jsonify(user=m.User.dump(me))
		resp.headers['Cache-Control'] = 'max-age=0, must-revalidate'
		return resp

	@app.route('/health-check')
	def health_check():
		return make_response('OK', 200, {'Content-Type': 'text/plain'})

	@app.route('/logout')
	def logout():
		@after_this_request
		def clear_cookie(resp):
			resp.set_cookie(current_app.config['APP_COOKIE_NAME'])
			return resp
		return redirect(app.config['AUTHENTICATION_LOGIN_URL'])

	@app.route('/')
	def index():
		fpath = os.path.join(os.path.dirname(__file__), 'index.html')
		return send_file(fpath)

	return app

