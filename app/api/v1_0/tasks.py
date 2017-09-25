
from flask import request, session, jsonify

import db.model as m
from db.db import SS
from app.api import api, caps
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

_name = __file__.split('/')[-1].split('.')[0]

@bp.route(_name + '/')
@api
# @caps()
def get_tasks():
	'''
	returns a list of matched tasks
	'''
	tasks = m.Task.query.all()
	return jsonify(tasks=m.Task.dump(tasks))


@bp.route(_name + '/<int:taskId>')
@api
# @caps()
def get_task(taskId):
	'''
	returns specified task
	'''
	task = m.Task.query.get(taskId)
	if not task:
		raise InvalidUsage(_('task {0} not found').format(taskId), 404)
	return jsonify(task=m.Task.dump(task))

@bp.route(_name + '/<int:taskId>/subtasks/')
@api
# @caps()
def get_task_sub_tasks(taskId):
	subTasks = m.SubTask.query.filter(m.SubTask.taskId==taskId).all()
	return jsonify(subTasks=m.SubTask.dump(subTasks))
