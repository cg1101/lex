
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import *

metadata = sa.MetaData()

t_script = sa.Table('script', metadata,
	sa.Column('script_id', INTEGER, primary_key=True, autoincrement=True, key=u'scriptId', doc=''),
	sa.Column('script_word_code', CHAR(4), nullable=False, key=u'scriptCode', doc=''),
	sa.Column('script_number_code', CHAR(3), nullable=False, key=u'scriptNumber', doc=''),
	sa.Column('script_name', TEXT, nullable=False, key=u'name', doc=''),
)

t_language = sa.Table('language', metadata,
	sa.Column('language_id', INTEGER, primary_key=True, autoincrement=True, key=u'dialectId', doc=''),
	sa.Column('language_name', TEXT, nullable=False, unique=True, key=u'name', doc=''),
	sa.Column('iso_language', CHAR(3), nullable=True, key=u'langCode', doc=''),
	sa.Column('iso_country', CHAR(3), nullable=True, key=u'countryCode', doc=''),
	sa.Column('script_id', INTEGER, sa.ForeignKey('script.scriptId'), nullable=True, key=u'scriptId', doc=''),
	sa.Column('directionality', BOOLEAN, nullable=False, server_default=sa.text('TRUE'), key=u'ltr', doc=''),
	sa.Column('romanisation', TEXT, nullable=True, key=u'romanizationScheme', doc=''),
)

t_phonetic_alphabet = sa.Table('phonetic_alphabet', metadata,
	sa.Column('alphabet_id', INTEGER, primary_key=True, autoincrement=True, key=u'alphabetId', doc=''),
	sa.Column('alphabet_name', TEXT, nullable=False, unique=True, key=u'name', doc=''),
	sa.Column('link', TEXT, nullable=False, unique=True, key=u'manPageUrl', doc=''),
	sa.Column('language_id', INTEGER, sa.ForeignKey('language.dialectId'), nullable=False, key=u'dialectId', doc=''),
	sa.Column('current', BOOLEAN, nullable=False, server_default=sa.text('TRUE'), key=u'current', doc=''),
)

t_phonetic_graphemes = sa.Table('phonetic_graphemes', metadata,
	sa.Column('phonetic_grapheme_id', INTEGER, primary_key=True, autoincrement=True, key=u'graphemeId', doc=''),
	sa.Column('ipa_id', TEXT, nullable=False, key=u'appenKey', doc=''),
	sa.Column('alphabet_id', INTEGER, sa.ForeignKey('phonetic_alphabet.alphabetId'), nullable=False, key=u'alphabetId', doc=''),
	sa.Column('grapheme', TEXT, nullable=False, key=u'sampa', doc=''),
	sa.Column('orthography', TEXT, nullable=True, key=u'orthography', doc=''),
	sa.Column('romanised_form', TEXT, nullable=True, key=u'romanization', doc=''),
)

t_alphabet_phoneme_map = sa.Table('alphabet_phoneme_map', metadata,
	sa.Column('alphabet_id', INTEGER, nullable=False, key=u'alphabetId', doc=''),
	sa.Column('phonetic_grapheme_id', INTEGER, nullable=False, key=u'graphemeId', doc=''),
	sa.Column('example_word', TEXT, key=u'exampleWord', doc=''),
	sa.Column('example_transcription', TEXT, key=u'exampleTranscription', doc=''),
	sa.Column('example_romanised_word', TEXT, key=u'exampleRomanization', doc=''),
	sa.PrimaryKeyConstraint(u'alphabetId', u'graphemeId'),
	sa.ForeignKeyConstraint([u'alphabetId', u'graphemeId'], ['phonetic_graphemes.alphabetId', 'phonetic_graphemes.graphemeId']),
)

t_dev__symbols = sa.Table('symbols', metadata,
	sa.Column('key', TEXT, primary_key=True, key=u'key', doc=''),
	sa.Column('ipa_id', TEXT, nullable=True, key=u'appenKey', doc=''),
	sa.Column('type', TEXT, nullable=False, key=u'type', doc=''),
	sa.Column('symbol', TEXT, key=u'symbol', doc=''),
	sa.Column('ipa_number', TEXT, key=u'ipaNumber', doc=''),
	sa.Column('normalized', BOOLEAN, nullable=False, server_default=sa.text('FALSE'), key=u'normalized', doc=''),
	sa.Column('x_sampa', TEXT, key=u'xSampa', doc=''),
	sa.Column('appen_sampa', TEXT, key=u'appenSampa', doc=''),
	sa.Column('tags', ARRAY(TEXT), key=u'tags', doc=''),
	schema='dev',
)

t_phonology_rule = sa.Table('phonology_rule', metadata,
	sa.Column('phonology_rule_id', INTEGER, primary_key=True, key=u'ruleId', doc=''),
	sa.Column('phonology_rule_name', TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('phonology_rule_description', TEXT, key=u'description', doc=''),
	sa.Column('alphabet_id', sa.ForeignKey('phonetic_alphabet.alphabetId'),
		nullable=True, key=u'alphabetId', doc=''),
)

t_phonology_rule_sequence = sa.Table('phonology_rule_sequence', metadata,
	sa.Column('phonology_rule_sequence_id', INTEGER, primary_key=True, key=u'sequenceId', doc=''),
	sa.Column('phonology_rule_sequence_incorrect', TEXT, key=u'incorrect', doc=''),
	sa.Column('phonology_rule_sequence_correct', TEXT, key=u'correct', doc=''),
	sa.Column('phonology_rule_id', INTEGER, sa.ForeignKey('phonology_rule.ruleId'), nullable=False, key=u'ruleId', doc=''),
)

t_phonology_rule_exception = sa.Table('phonology_rule_exception', metadata,
	sa.Column('phonology_rule_exception_id', INTEGER, primary_key=True, key=u'exceptionId', doc=''),
	sa.Column('phonology_rule_id', INTEGER, sa.ForeignKey('phonology_rule.ruleId'), nullable=False, key=u'ruleId', doc=''),
	sa.Column('phonology_rule_exception_word', TEXT, key=u'word', doc=''),
	sa.Column('phonology_rule_exception_transcription', TEXT, key=u'tx', doc=''),
	sa.Column('user_id', INTEGER, nullable=False, key=u'userId', doc=''),
	sa.Column('review', BOOLEAN, key=u'needsReview', doc=''),
)


t_stress_rule = sa.Table('stress_rule', metadata,
	sa.Column('stress_rule_id', INTEGER, primary_key=True, key=u'ruleId', doc=''),
	sa.Column('stress_rule_name', TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('stress_rule_description', TEXT, key=u'description', doc=''),
	sa.Column('alphabet_id', sa.ForeignKey('phonetic_alphabet.alphabetId'),
		nullable=True, key=u'alphabetId', doc=''),
	sa.Column('stress_rule_sequence', TEXT, nullable=False, key=u'sequence', doc=''),
)

t_stress_rule_exception = sa.Table('stress_rule_exception', metadata,
	sa.Column('stress_rule_exception_id', INTEGER, primary_key=True, key=u'exceptionId', doc=''),
	sa.Column('stress_rule_id', INTEGER, sa.ForeignKey('stress_rule.ruleId'), nullable=False, key=u'ruleId', doc=''),
	sa.Column('stress_rule_exception_word', TEXT, key=u'word', doc=''),
	sa.Column('stress_rule_exception_transcription', TEXT, key=u'tx', doc=''),
	sa.Column('user_id', INTEGER, nullable=False, key=u'userId', doc=''),
	sa.Column('review', BOOLEAN, key=u'needsReview', doc=''),
)


t_syllabification_rule = sa.Table('syllabification_rule', metadata,
	sa.Column('syllabification_rule_id', INTEGER, primary_key=True, key=u'ruleId', doc=''),
	sa.Column('syllabification_rule_name', TEXT, nullable=False, key=u'name', doc=''),
	# sa.Column('syllabification_rule_description', TEXT, key=u'description', doc=''),
	sa.Column('alphabet_id', sa.ForeignKey('phonetic_alphabet.alphabetId'),
		nullable=True, key=u'alphabetId', doc=''),
)

t_syllabification_rule_sequence = sa.Table('syllabification_rule_sequence', metadata,
	sa.Column('syllabification_rule_sequence_id', INTEGER, primary_key=True, key=u'sequenceId', doc=''),
	sa.Column('syllabification_rule_sequence_correct', TEXT, key=u'correct', doc=''),
	sa.Column('syllabification_rule_id', INTEGER, sa.ForeignKey('syllabification_rule.ruleId'), nullable=False, key=u'ruleId', doc=''),
)

t_syllabification_rule_exception = sa.Table('syllabification_rule_exception', metadata,
	sa.Column('syllabification_rule_exception_id', INTEGER, primary_key=True, key=u'exceptionId', doc=''),
	sa.Column('syllabification_rule_id', INTEGER, sa.ForeignKey('syllabification_rule.ruleId'), nullable=False, key=u'ruleId', doc=''),
	sa.Column('syllabification_rule_exception_word', TEXT, key=u'word', doc=''),
	sa.Column('syllabification_rule_exception_transcription', TEXT, key=u'tx', doc=''),
	sa.Column('user_id', INTEGER, nullable=False, key=u'userId', doc=''),
	sa.Column('review', BOOLEAN, key=u'needsReview', doc=''),
)


t_vowelisation_rule = sa.Table('vowelisation_rule', metadata,
	sa.Column('vowelisation_rule_id', INTEGER, primary_key=True, key=u'ruleId', doc=''),
	sa.Column('vowelisation_rule_name', TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('vowelisation_rule_description', TEXT, key=u'description', doc=''),
	sa.Column('alphabet_id', sa.ForeignKey('phonetic_alphabet.alphabetId'),
		nullable=True, key=u'alphabetId', doc=''),
)

t_vowelisation_rule_sequence = sa.Table('vowelisation_rule_sequence', metadata,
	sa.Column('vowelisation_rule_sequence_id', INTEGER, primary_key=True, key=u'sequenceId', doc=''),
	sa.Column('vowelisation_rule_sequence_incorrect', TEXT, key=u'incorrect', doc=''),
	sa.Column('vowelisation_rule_sequence_correct', TEXT, key=u'correct', doc=''),
	sa.Column('vowelisation_rule_id', INTEGER, sa.ForeignKey('vowelisation_rule.ruleId'), nullable=False, key=u'ruleId', doc=''),
)

t_vowelisation_rule_exception = sa.Table('vowelisation_rule_exception', metadata,
	sa.Column('vowelisation_rule_exception_id', INTEGER, primary_key=True, key=u'exceptionId', doc=''),
	sa.Column('vowelisation_rule_id', INTEGER, sa.ForeignKey('vowelisation_rule.ruleId'), nullable=False, key=u'ruleId', doc=''),
	sa.Column('vowelisation_rule_exception_word', TEXT, key=u'word', doc=''),
	sa.Column('vowelisation_rule_exception_vowelised_word', TEXT, key=u'vowelisedWord', doc=''),
	sa.Column('user_id', INTEGER, nullable=False, key=u'userId', doc=''),
	sa.Column('review', BOOLEAN, key=u'needsReview', doc=''),
)

t_project = sa.Table('project', metadata,
	sa.Column('project_id', INTEGER, primary_key=True, autoincrement=False, key=u'projectId', doc=''),
	sa.Column('project_name', TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('current', BOOLEAN, nullable=False, server_default=sa.text('TRUE'), key=u'current', doc=''),
	sa.Column('link', TEXT, key=u'url', doc=''),
)

t_task_type = sa.Table('task_type', metadata,
	sa.Column('type_id', INTEGER, primary_key=True, key=u'taskTypeId', doc=''),
	sa.Column('type_name', TEXT, nullable=False, key=u'name', doc=''),
)

t_task = sa.Table('task', metadata,
	sa.Column('task_id', INTEGER, primary_key=True, autoincrement=False, key=u'taskId', doc=''),
	sa.Column('project_id', INTEGER, sa.ForeignKey('project.projectId'), nullable=False, key=u'projectId', doc=''),
	sa.Column('alphabet_id', INTEGER, sa.ForeignKey('phonetic_alphabet.alphabetId'), nullable=False, key=u'alphabetId', doc=''),
	sa.Column('task_name', TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('conventions_link', TEXT, key=u'conventionsUrl', doc=''),
	sa.Column('type_id', INTEGER, sa.ForeignKey('task_type.taskTypeId'), nullable=False, key=u'taskTypeId', doc=''),
	sa.Column('link', TEXT, key=u'url', doc=''),
	sa.Column('second_headword_field', BOOLEAN, nullable=False, server_default=sa.text('FALSE'), key=u'hasSecondHeadword', doc=''),
)

__all__ = [name for name in locals().keys()
		if name.startswith('t_') or name.startswith('j_')]
__all__.insert(0, 'metadata')
