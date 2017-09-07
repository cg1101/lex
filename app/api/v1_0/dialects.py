
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
def get_dialects():
	'''
	returns a list of matched dialects
	'''
	dialects = m.Dialect.query.all()
	return jsonify(dialects=m.Dialect.dump(dialects))


@bp.route(_name + '/<int:dialectId>', methods=['GET'])
@api
# @caps()
def get_dialect(dialectId):
	'''
	returns specified dialect
	'''
	dialect = m.Dialect.query.get(dialectId)
	if not dialect:
		raise InvalidUsage(_('dialect {0} not found').format(dialectId), 404)
	return jsonify(dialect=m.Dialect.dump(dialect))

