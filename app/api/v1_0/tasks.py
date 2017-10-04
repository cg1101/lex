
from flask import request, session, jsonify

import db.model as m
from db.db import SS
from app.api import api, caps, MyForm, Field
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

_name = __file__.split('/')[-1].split('.')[0]

@bp.route(_name + '/')
@api
# @caps()
def get_tasks():
	tasks = m.Task.query.all()
	return jsonify(tasks=m.Task.dump(tasks))


@bp.route(_name + '/<int:taskId>')
@api
# @caps()
def get_task(taskId):
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


@bp.route(_name + '/<int:taskId>/tags/')
@api
# @caps()
def get_task_tags(taskId):
	task = m.Task.query.get(taskId)
	if not task:
		raise InvalidUsage(_('task {0} not found').format(taskId), 404)
	return jsonify(tags=m.Tag.dump(task.tags))


@bp.route(_name + '/<int:taskId>/loads/')
@api
# @caps()
def get_task_loads(taskId):
	loads = m.Load.query.filter(m.Load.taskId==taskId).all()
	return jsonify(loads=m.Load.dump(loads))


@bp.route(_name + '/<int:taskId>/check-headwords', methods=['POST'])
@api
# @caps()
def check_headwords(taskId):
	task = m.Task.query.get(taskId)
	if not task:
		raise InvalidUsage(_('task {0} not found').format(taskId), 404)
	if task.taskType != 'Spelling':
		raise InvalidUsage(_('task {0} has unexpected task type').format(taskId))
	data = MyForm(
		Field('headwords', is_mandatory=True,)
	).get_data()
	loaded = {}
	for r in SS.query(m.RawPiece.rawPieceId, m.RawPiece.rawText, m.RawPiece.meta
			).distinct(m.RawPiece.rawText
			).order_by(m.RawPiece.rawText, m.RawPiece.rawPieceId.desc()
			).filter(m.RawPiece.taskId==taskId).all():
		loaded[r.rawText] = r
	headwords = {}
	for hw in data['headwords']:
		headwords[hw] = loaded.get(hw, None)
	return jsonify(headwords=headwords)


@bp.route(_name + '/<int:taskId>/save-headwords', methods=['POST'])
@api
# @caps()
def save_headwords(taskId):
	task = m.Task.query.get(taskId)
	if not task:
		raise InvalidUsage(_('task {0} not found').format(taskId), 404)
	if task.taskType != 'Spelling':
		raise InvalidUsage(_('task {0} has unexpected task type').format(taskId))
	data = MyForm(
		Field('headwords', is_mandatory=True,)
	).get_data()
	load = m.Load(taskId=taskId, createdBy=699)
	SS.add(load)
	SS.flush()
	rawPieces = []
	for i, r in enumerate(data['headwords']):
		assemblyContext = 'L_%05d_%05d' % (load.loadId, i)
		allocationContext = 'L_%05d' % load.loadId
		try:
			del r['meta']
		except KeyError:
			pass
		print r
		rawPiece = m.RawPiece(taskId=taskId, loadId=load.loadId,
			assemblyContext=assemblyContext,
			allocationContext=allocationContext,
			words=1,
			**r)
		rawPieces.append(rawPiece)
		SS.add(rawPiece)
	SS.flush()
	return jsonify(rawPieces=m.RawPiece.dump(rawPieces))

