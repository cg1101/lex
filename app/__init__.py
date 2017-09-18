#!/usr/bin/env python

import os
import re

from flask import Flask, session, request, after_this_request,\
		redirect, jsonify, make_response, url_for, current_app, g,\
		send_file
from flask_cors import CORS

from config import config
import db.model as m
from db.db import SS
from db import database as db
# from .auth import MyAuthMiddleWare
# from .i18n import get_text as _


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	db.init_app(app)

	CORS(app, resources={'/api/1.0/*': {'origins': '*'}})

	# app.wsgi_app = MyAuthMiddleWare(app.wsgi_app,
	# 	app.config['AUTHENTICATION_LOGIN_URL'],
	# 	public_prefixes=['/static/', '/webservices', '/logout'],
	# 	json_prefixes=['/api/'],
	# )

	# public_url_patterns = map(re.compile, [
	# 	'/static/',
	# 	'/favicon.ico',
	# 	'/edm',
	# 	'/webservices',
	# 	'/logout',
	# 	'/authorization_response',
	# 	'/health-check',
	# ])
	# json_url_patterns = map(re.compile, [
	# 	'/whoami',
	# 	'/api'
	# ])

	from app.api import api_1_0
	# from app.edm import edm
	# from app.tagimages import tagimages
	# from app.webservices import webservices
	# from app.views import views
	app.register_blueprint(api_1_0, url_prefix='/api/1.0/')
	# app.register_blueprint(edm, url_prefix='/edm')
	# app.register_blueprint(tagimages, url_prefix='/tagimages')
	# app.register_blueprint(webservices, url_prefix='/webservices')
	# app.register_blueprint(views, url_prefix='')

	# @app.before_request
	# def get_current_user():
	# 	data = request.environ.get('myauthmiddleware', None)
	# 	if not data:
	# 		user = User.query.get(699)
	# 	else:
	# 		user = User.query.get(data['REMOTE_USER_ID'])
	# 		session['current_user'] = user

	# @app.after_request
	# def set_cookie_if_necessary(resp):
	# 	if g.get('update_cookie', False):
	# 		current_app.logger.debug('trying to set cookie as instructed')
	# 		try:
	# 			me = session['current_user']
	# 			caps = session['current_user_caps']
	# 			user_type = session['current_user_type']
	# 			roles = session['current_user_roles']
	# 			data = {
	# 				'REMOTE_USER_ID': me.userId,
	# 				'REMOTE_USER_NAME': me.userName,
	# 				'CAPABILITIES': caps,
	# 				'USER_TYPE': user_type,
	# 				'ROLES': roles,
	# 			}
	# 			value = auth.encode_cookie(data,
	# 				current_app.config['APP_COOKIE_SECRET'], timeout=0)
	# 			resp.set_cookie(current_app.config['APP_COOKIE_NAME'], value)
	# 		except Exception, e:
	# 			current_app.logger.debug('error setting cookie {}'.format(e))
	# 			pass
	# 	session['current_user'] = None
	# 	return resp

	# @app.route('/whoami')
	# def who_am_i():
	# 	me = session['current_user']
	# 	ao_url = util.tiger.get_url_root().replace('global', 'online')
	# 	if ao_url.endswith('online.appen.com'):
	# 		ao_url = ao_url.replace('/online.appen.com', '/appenonline.appen.com.au')
	# 	resp = jsonify(
	# 		user=m.User.dump(me, use='full'),
	# 		caps=session['current_user_caps'],
	# 		userType=session['current_user_type'],
	# 		roles=session['current_user_roles'],
	# 		runtimeEnvironment={
	# 			'tiger': util.tiger.get_url_root(),
	# 			'edm': util.edm.get_url_root(),
	# 			'go': util.go.get_url_root(),
	# 			'ao': ao_url,
	# 		}
	# 	)
	# 	resp.headers['Cache-Control'] = 'max-age=0, must-revalidate'
	# 	return resp


	@app.route('/health-check')
	def health_check():
		return make_response('OK', 200, {'Content-Type': 'text/plain'})

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

	@app.route('/')
	def index():
		fpath = os.path.join(os.path.dirname(__file__), 'index.html')
		return send_file(fpath)

	return app

