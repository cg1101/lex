#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from application import application as app
from db import database as db

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

# def make_shell_context():
# 	return dict(app=app, db=db, User=User, Role=Role)
# manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def list():
	for rule in app.url_map.iter_rules():
		print(str(rule), 'methods:', ','.join(rule.methods), '->', rule.endpoint)


if __name__ == '__main__':
	manager.run()
