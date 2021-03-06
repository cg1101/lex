
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
def get_projects():
	projects = m.Project.query.all()
	return jsonify(projects=m.Project.dump(projects))


@bp.route(_name + '/<int:projectId>')
@api
# @caps()
def get_project(projectId):
	project = m.Project.query.get(projectId)
	if not project:
		raise InvalidUsage(_('project {0} not found').format(projectId), 404)
	return jsonify(project=m.Project.dump(project))


@bp.route(_name + '/<int:projectId>/tasks/')
@api
# @caps()
def get_project_tasks(projectId):
	tasks = m.Task.query.filter(m.Task.projectId==projectId).all()
	return jsonify(tasks=m.Task.dump(tasks))
