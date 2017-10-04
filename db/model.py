
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref, synonym, deferred, column_property, object_session
from marshmallow import Schema, fields

from . import database, mode
from .db import SS
from .db import database as db
from schema import *


def set_schema(cls, schema_class, schema_key=None):
	if not issubclass(schema_class, Schema):
		raise TypeError('schema must be subclass of Schema')
	registry = cls.__dict__.get('_schema_registry', None)
	if registry is None:
		cls._schema_registry = {}
	cls._schema_registry[schema_key] = schema_class


def dump(cls, obj, use=None, extra=None, only=(), exclude=(),
	prefix=u'', strict=False, context=None, load_only=(), **kwargs):
	try:
		schema_class = cls._schema_registry.get(use, None)
	except:
		schema_class = None
	if schema_class is None:
		raise RuntimeError('schema class not found for {0}: key {1}'\
			.format(cls.__name__, use))
	s = schema_class(extra=extra, only=only, exclude=exclude,
			prefix=prefix, strict=strict, context=context)
	if isinstance(obj, list):
		many = True
	else:
		many = False
	marshal_result = s.dump(obj, many=many, **kwargs)
	return marshal_result.data

if mode == 'app':
	Base = database.Model
else:
	class MyBase(object):
		pass
	Base = declarative_base(cls=MyBase, metadata=metadata)
	Base.query = SS.query_property()

Base.set_schema = classmethod(set_schema)
Base.dump = classmethod(dump)


_names = set(locals().keys()) | {'_names'}


#
# Define model class and its schema (if needed) below
#
##########################################################################

class Symbol(Base):
	__table__ = t_dev__symbols
	@property
	def sampa(self):
		return self.appenSampa or self.xSampa or ''

class SymbolSchema(Schema):
	class Meta:
		fields = ('key', 'appenKey', 'type', 'symbol', 'ipaNumber', 'xSampa', 'appenSampa', 'tags')

class KeyMap(object):
	_singleton = None
	def __init__(self, *args, **kwargs):
		raise RuntimeError('KeyMap must not be instantiated directly')
	@classmethod
	def get_map(klass):
		if klass._singleton is None:
			s = klass._singleton = super(KeyMap, klass).__new__(klass)
			s._key_map = {}
			s._runtime_map = {}
			for symbol in Symbol.query.filter(Symbol.appenKey!=None).all():
				s._key_map[symbol.appenKey] = symbol.key
		return klass._singleton
	def get_key(self, raw_ipa_id):
		ipa_id = raw_ipa_id
		if ipa_id.endswith(';0'):
			ipa_id = ipa_id[:-1]
		if self._key_map.has_key(ipa_id):
			return self._key_map[ipa_id]
		if self._runtime_map.has_key(ipa_id):
			return self._runtime_map[ipa_id]
		ids = ipa_id.rstrip(';').split(';')
		buf = []
		for i in ids:
			i = i + ';'
			try:
				buf.append(self._key_map[i])
			except KeyError:
				raise ValueError('{} in {} not defined'.format(i, raw_ipa_id))
		return buf


# WritingScript
class WritingScript(Base):
	__table__ = t_script

class WritingScriptSchema(Schema):
	class Meta:
		fields = ('scriptId', 'name', 'scriptCode', 'scriptNumber')


# Dialect
class Dialect(Base):
	__table__ = t_language
	script = relationship('WritingScript')

class DialectSchema(Schema):
	script = fields.Nested('WritingScriptSchema')
	class Meta:
		fields = ('dialectId', 'name', 'langCode', 'countryCode', 'ltr',
			'romanizationScheme', 'scriptId', 'script')


# Alphabet
class Alphabet(Base):
	__table__ = t_phonetic_alphabet
	dialect = relationship('Dialect')
	graphemes = relationship('Grapheme', backref='alphabet')
	phonologyRules = relationship('PhonologyRule')
	stressRules = relationship('StressRule')
	syllabificationRules = relationship('SyllabificationRule')
	vowelisationRules = relationship('VowelisationRule')

class AlphabetSchema(Schema):
	dialect = fields.Nested('DialectSchema', exclude=('dialectId',))
	graphemes = fields.Nested('GraphemeSchema', many=True, exclude=('alphabetId',))
	phonologyRules = fields.Nested('PhonologyRuleSchema', many=True, exclude=('alphabetId',))
	stressRules = fields.Nested('StressRuleSchema', many=True, exclude=('alphabetId',))
	syllabificationRules = fields.Nested('SyllabificationRuleSchema', many=True, exclude=('alphabetId',))
	vowelisationRules = fields.Nested('VowelisationRuleSchema', many=True, exclude=('alphabetId',))
	class Meta:
		fields = ('alphabetId', 'name', 'manPageUrl', 'current', 'dialectId')

class Alphabet_FullSchema(AlphabetSchema):
	class Meta:
		fields = ('alphabetId', 'name', 'manPageUrl', 'current', 'dialectId',
			'dialect', 'graphemes',
			'phonologyRules', 'stressRules', 'syllabificationRules', 'vowelisationRules')


# Grapheme
class Grapheme(Base):
	__table__ = t_phonetic_graphemes
	dataBag = relationship('GraphemeDataBag', uselist=False)
	exampleWord = association_proxy('dataBag', 'exampleWord')
	exampleTranscription = association_proxy('dataBag', 'exampleTranscription')
	exampleRomanization = association_proxy('dataBag', 'exampleRomanization')
	ipa_id = synonym('appenKey')

	@property
	def key(self):
		if getattr(self, '_phone_key', None) is None:
			m = KeyMap.get_map()
			key = KeyMap.get_map().get_key(self.appenKey)
			setattr(self, '_phone_key', key)
		if isinstance(self._phone_key, list):
			return ''.join(self._phone_key)
		return self._phone_key

class GraphemeSchema(Schema):
	class Meta:
		fields = ('graphemeId', 'alphabetId', 'appenKey',
			'sampa', 'orthography', 'romanization',
			'exampleWord', 'exampleTranscription', 'exampleRomanization')


# GraphemeDataBag
class GraphemeDataBag(Base):
	__table__ = t_alphabet_phoneme_map


# PhonologyRule
class PhonologyRule(Base):
	__table__ = t_phonology_rule
	sequences = relationship('PhonologyRuleSequence')
	@property
	def type(self):
		return 'phonology'

class PhonologyRuleSchema(Schema):
	sequences = fields.Nested('PhonologyRuleSequenceSchema', many=True, exclude=('ruleId',))
	class Meta:
		fields = ('ruleId', 'type', 'name', 'description', 'alphabetId', 'sequences')

class PhonologyRuleSequence(Base):
	__table__ = t_phonology_rule_sequence

class PhonologyRuleSequenceSchema(Schema):
	class Meta:
		fields = ('ruleId', 'sequenceId', 'correct', 'incorrect')

# StressRule
class StressRule(Base):
	__table__ = t_stress_rule
	@property
	def type(self):
		return 'stress'

class StressRuleSchema(Schema):
	sequences = fields.Method('get_sequences')
	def get_sequences(self, obj):
		return [dict(sequenceId=obj.ruleId, correct=obj.sequence)]
	class Meta:
		fields = ('ruleId', 'type', 'name', 'description', 'alphabetId', 'sequences')

# SyllabificationRule
class SyllabificationRule(Base):
	__table__ = t_syllabification_rule
	sequences = relationship('SyllabificationRuleSequence')
	@property
	def description(self):
		return None
	@property
	def type(self):
		return 'syllabification'

class SyllabificationRuleSchema(Schema):
	sequences = fields.Nested('SyllabificationRuleSequenceSchema', many=True, exclude=('ruleId',))
	class Meta:
		fields = ('ruleId', 'type', 'name', 'description', 'alphabetId', 'sequences')

class SyllabificationRuleSequence(Base):
	__table__ = t_syllabification_rule_sequence

class SyllabificationRuleSequenceSchema(Schema):
	class Meta:
		fields = ('ruleId', 'sequenceId', 'correct')

# VowelisationRule
class VowelisationRule(Base):
	__table__ = t_vowelisation_rule
	sequences = relationship('VowelisationRuleSequence')
	@property
	def type(self):
		return 'vowelisation'

class VowelisationRuleSchema(Schema):
	sequences = fields.Nested('VowelisationRuleSequenceSchema', many=True, exclude=('ruleId',))
	class Meta:
		fields = ('ruleId', 'type', 'name', 'description', 'alphabetId', 'sequences')

class VowelisationRuleSequence(Base):
	__table__ = t_vowelisation_rule_sequence

class VowelisationRuleSequenceSchema(Schema):
	class Meta:
		fields = ('ruleId', 'sequenceId', 'correct', 'incorrect')

class User(Base):
	__table__ = t_users


class Project(Base):
	__table__ = t_project

class ProjectSchema(Schema):
	class Meta:
		fields = ('projectId', 'name', 'current', 'url')

class TaskType(Base):
	__table__ = t_task_type

class Task(Base):
	__table__ = t_task
	_taskType = relationship('TaskType')
	taskType = association_proxy('_taskType', 'name')
	alphabet = relationship('Alphabet')
	tags = relationship('Tag', lazy=True,
		secondary='tag_task_map',
		primaryjoin='Task.taskId==TaskTag.taskId',
		secondaryjoin='TaskTag.tagId==Tag.tagId',
	)
	words = relationship('Word', lazy=True,
		secondary='word_task_map',
		primaryjoin='Task.taskId==TaskWord.taskId',
		secondaryjoin='TaskWord.wordId==Word.wordId',
	)
	imports = relationship('ImportedFile', lazy=True)
	exports = relationship('ExportedFile', lazy=True)

class TaskSchema(Schema):
	class Meta:
		fields = ('taskId', 'name', 'projectId', 'taskTypeId', 'taskType',
			'alphabetId', 'url', 'conventionsUrl', 'hasSecondHeadword')

class WorkType(Base):
	__table__ = t_subtask_type

class WorkTypeSchema(Schema):
	class Meta:
		fields = ('workTypeId', 'name')

class SubTask(Base):
	__table__ = t_subtask
	_workType = relationship('WorkType')
	workType = association_proxy('_workType', 'name')

class SubTaskSchema(Schema):
	class Meta:
		fields = ('subTaskId', 'name', 'description', 'taskId', 'workTypeId',
			'workType', 'batchSize')

class Tag(Base):
	__table__ = t_tag

class TagSchema(Schema):
	class Meta:
		fields = ('tagId', 'name')

class TaskTag(Base):
	__table__ = t_tag_task_map

class TaskWord(Base):
	__table__ = t_word_task_map

class ImportedFile(Base):
	__table__ = t_task_lexicon_import_map
	data = deferred(t_task_lexicon_import_map.c.data)

class ExportedFile(Base):
	__table__ = t_task_lexicon_export_map
	data = deferred(t_task_lexicon_export_map.c.data)

class Consonant(Base):
	__table__ = t_consonant_description

class Diacritic(Base):
	__table__ = t_diacritic_description

class Suprasegmental(Base):
	__table__ = t_suprasegmental_description

class Vowel(Base):
	__table__ = t_vowel_description

class Word(Base):
	__table__ = t_word

class RawPiece(Base):
	__table__ = t_rawpieces

class RawPieceSchema(Schema):
	class Meta:
		fields = ('rawPieceId', 'rawText', 'hypothesis', 'words',
			'assemblyContext', 'allocationContext', 'loadId')
class Load(Base):
	__table__ = t_loads

class LoadSchema(Schema):
	class Meta:
		fields = ('loadId', 'createdAt', 'createdBy', 'taskId')

##########################################################################
#
# Define model class and its schema (if needed) above
#

__all__ = list(set(locals().keys()) - _names)

for schema_name in [i for i in __all__ if i.endswith('Schema')]:
	klass_name = schema_name[:-6]
	if klass_name.find('_') >= 0:
		klass_name, schema_key = klass_name.split('_', 1)
		schema_key = schema_key.lower()
	else:
		schema_key = ''
	assert klass_name
	klass = locals()[klass_name]
	schema = locals()[schema_name]
	klass.set_schema(schema, schema_key or None)
