
from flask import request, session, jsonify

import db.model as m
from db.db import SS
from app.api import api, caps
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

_name = __file__.split('/')[-1].split('.')[0]

@bp.route(_name + '/', methods=['GET'])
@api
# @caps()
def get_projects():
	'''
	returns a list of matched projects
	'''
	projects = m.Project.query.all()
	return jsonify(projects=m.Project.dump(projects))


@bp.route(_name + '/<int:projectId>', methods=['GET'])
@api
# @caps()
def get_project(projectId):
	'''
	returns specified project
	'''
	project = m.Project.query.get(projectId)
	if not project:
		raise InvalidUsage(_('project {0} not found').format(projectId), 404)
	return jsonify(project=m.Project.dump(project))

