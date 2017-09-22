
import os

class Config:
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URI')
			or 'postgresql://dbserver/appenlex')
	AUTHENTICATION_LOGIN_URL = os.environ['AUTHENTICATION_LOGIN_URL']
	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True

class ProductionConfig(Config):
	SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig,
}
