
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
def get_alphabets():
	alphabets = m.Alphabet.query.all()
	return jsonify(alphabets=m.Alphabet.dump(alphabets))


@bp.route(_name + '/<int:alphabetId>')
@api
# @caps()
def get_alphabet(alphabetId):
	alphabet = m.Alphabet.query.get(alphabetId)
	if not alphabet:
		raise InvalidUsage(_('alphabet {0} not found').format(alphabetId), 404)
	return jsonify(alphabet=m.Alphabet.dump(alphabet, use='full'))

