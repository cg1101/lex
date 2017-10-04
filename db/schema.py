
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

t_dev__users = sa.Table('users', metadata,
	sa.Column('userid', INTEGER, primary_key=True, autoincrement=False, key=u'userId', doc=''),
	sa.Column('emailaddress', TEXT, nullable=False, key=u'emailAddress', doc=''),
	sa.Column('active', BOOLEAN, nullable=False, server_default=sa.text('TRUE'), key=u'isActive', doc=''),
	sa.Column('familyname', TEXT, key=u'familyName', doc=''),
	sa.Column('givenname', TEXT, key=u'givenName', doc=''),
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

t_tag = sa.Table('tag', metadata,
	sa.Column('tag_id', INTEGER, primary_key=True, autoincrement=True, key=u'tagId', doc=''),
	sa.Column('tag_name', TEXT, nullable=False, key=u'name', doc=''),
)

t_tag_task_map = sa.Table('tag_task_map', metadata,
	sa.Column('tag_id', INTEGER, sa.ForeignKey('tag.tagId'), nullable=False, key=u'tagId', doc=''),
	sa.Column('task_id', INTEGER, sa.ForeignKey('task.taskId'), nullable=False, key=u'taskId', doc=''),
	sa.PrimaryKeyConstraint(u'taskId', u'tagId'),
)

t_tag_word_map = sa.Table('tag_word_map', metadata,
)

t_users = sa.Table('users', metadata,
	sa.Column('user_id', INTEGER, primary_key=True, autoincrement=False, key=u'userId', doc=''),
)

t_subtask_type = sa.Table('subtask_type', metadata,
	sa.Column('type_id', INTEGER, primary_key=True, key=u'workTypeId', doc=''),
	sa.Column('type_name', TEXT, nullable=False, key=u'name', doc=''),
)

t_subtask = sa.Table('subtask', metadata,
	sa.Column('subtask_id', INTEGER, primary_key=True, key='subTaskId', doc=''),
	sa.Column('task_id', INTEGER, sa.ForeignKey('task.taskId'), nullable=False, key=u'taskId', doc=''),
	sa.Column('subtask_name', TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('batch_size', INTEGER, nullable=False, server_default=sa.text('100'), key=u'batchSize', doc=''),
	sa.Column('subtask_description', TEXT, key=u'description', doc=''),
	sa.Column('subtask_query', TEXT, key=u'searchQuery', doc=''),
	sa.Column('expected_throughput', INTEGER, key=u'throughput', doc=''),
	sa.Column('piecework_payment', BOOLEAN, nullable=False, server_default=sa.text('FALSE'), key=u'pieceMeal', doc=''),
	sa.Column('type_id', INTEGER, sa.ForeignKey('subtask_type.workTypeId'), nullable=True, key=u'workTypeId', doc=''),
)

t_word = sa.Table('word', metadata,
	sa.Column('word_id', INTEGER, primary_key=True, autoincrement=True, key=u'wordId', doc=''),
	sa.Column('alphabet_id', INTEGER, sa.ForeignKey('phonetic_alphabet.alphabetId'), key=u'alphabetId', doc=''),
	sa.Column('headword', TEXT, key=u'headword', doc=''),
)

t_word_subtask_map = sa.Table('word_subtask_map', metadata,
	sa.Column('subtask_id', INTEGER, sa.ForeignKey('subtask.subTaskId'), nullable=False, key=u'subTaskId', doc=''),
	sa.Column('word_id', INTEGER, sa.ForeignKey('word.wordId'), nullable=False, key=u'wordId', doc=''),
	sa.Column('variant_number', INTEGER, nullable=False, key=u'ranking', doc=''),
	sa.Column('user_id', INTEGER, sa.ForeignKey('users.userId'), key=u'userId', doc=''),
	sa.Column('timestamp', TIMESTAMP(timezone=True), key=u'timestamp', doc=''),
	sa.Column('expiry', TIMESTAMP(timezone=True), key=u'expiry', doc=''),
	sa.PrimaryKeyConstraint(u'subTaskId', u'wordId', u'ranking'),
)

t_word_task_map = sa.Table('word_task_map', metadata,
	sa.Column('task_id', INTEGER, sa.ForeignKey('task.taskId'), nullable=False, key=u'taskId', doc=''),
	sa.Column('variant_number', INTEGER, nullable=False, key=u'ranking', doc=''),
	sa.Column('word_id', INTEGER, sa.ForeignKey('word.wordId'), nullable=False, key=u'wordId', doc=''),
	sa.PrimaryKeyConstraint(u'taskId', u'wordId', u'ranking'),
)

t_subtask_user_map = sa.Table('subtask_user_map', metadata,
	sa.Column('user_id', INTEGER, sa.ForeignKey('users.userId'), nullable=False, key=u'userId', doc=''),
	sa.Column('subtask_id', INTEGER, sa.ForeignKey('subtask.subTaskId'), nullable=False, key=u'subTaskId', doc=''),
	sa.PrimaryKeyConstraint(u'subTaskId', u'userId'),
)

t_consonant_description = sa.Table('consonant_description', metadata,
	sa.Column('ipa_id', TEXT, primary_key=True, key=u'appenKey', doc=''),
	sa.Column('alveolar', BOOLEAN, nullable=False, key=u'alveolar', doc=''),
	sa.Column('fricative', BOOLEAN, nullable=False, key=u'fricative', doc=''),
	sa.Column('tap', BOOLEAN, nullable=False, key=u'tap', doc=''),
	sa.Column('lateral_flap', BOOLEAN, nullable=False, key=u'lateral_flap', doc=''),
	sa.Column('affricate', BOOLEAN, nullable=False, key=u'affricate', doc=''),
	sa.Column('voiceless', BOOLEAN, nullable=False, key=u'voiceless', doc=''),
	sa.Column('nasal', BOOLEAN, nullable=False, key=u'nasal', doc=''),
	sa.Column('lateral_fricative', BOOLEAN, nullable=False, key=u'lateral_fricative', doc=''),
	sa.Column('bilabial', BOOLEAN, nullable=False, key=u'bilabial', doc=''),
	sa.Column('glottal', BOOLEAN, nullable=False, key=u'glottal', doc=''),
	sa.Column('approximant', BOOLEAN, nullable=False, key=u'approximant', doc=''),
	sa.Column('voiced', BOOLEAN, nullable=False, key=u'voiced', doc=''),
	sa.Column('retroflex', BOOLEAN, nullable=False, key=u'retroflex', doc=''),
	sa.Column('click', BOOLEAN, nullable=False, key=u'click', doc=''),
	sa.Column('implosive', BOOLEAN, nullable=False, key=u'implosive', doc=''),
	sa.Column('epiglottal', BOOLEAN, nullable=False, key=u'epiglottal', doc=''),
	sa.Column('trill', BOOLEAN, nullable=False, key=u'trill', doc=''),
	sa.Column('palatal', BOOLEAN, nullable=False, key=u'palatal', doc=''),
	sa.Column('velar', BOOLEAN, nullable=False, key=u'velar', doc=''),
	sa.Column('plosive', BOOLEAN, nullable=False, key=u'plosive', doc=''),
	sa.Column('uvular', BOOLEAN, nullable=False, key=u'uvular', doc=''),
	sa.Column('lateral_approximant', BOOLEAN, nullable=False, key=u'lateral_approximant', doc=''),
	sa.Column('pharyngeal', BOOLEAN, nullable=False, key=u'pharyngeal', doc=''),
	sa.Column('palato_alveolar', BOOLEAN, nullable=False, key=u'palato_alveolar', doc=''),
	sa.Column('labiodental', BOOLEAN, nullable=False, key=u'labiodental', doc=''),
	sa.Column('labialised_approximant', BOOLEAN, nullable=False, key=u'labialised_approximant', doc=''),
	sa.Column('palatalised_affricate', BOOLEAN, nullable=False, key=u'palatalised_affricate', doc=''),
	sa.Column('dental', BOOLEAN, nullable=False, key=u'dental', doc=''),
	sa.Column('palatalised_fricative', BOOLEAN, nullable=False, key=u'palatalised_fricative', doc=''),
	sa.Column('flap', BOOLEAN, nullable=False, key=u'flap', doc=''),
)

t_diacritic_description = sa.Table('diacritic_description', metadata,
	sa.Column('ipa_id', TEXT, primary_key=True, key=u'appenKey', doc=''),
	sa.Column('raised', BOOLEAN, nullable=False, key=u'raised', doc=''),
	sa.Column('more_rounded', BOOLEAN, nullable=False, key=u'more_rounded', doc=''),
	sa.Column('bottom_tone', BOOLEAN, nullable=False, key=u'bottom_tone', doc=''),
	sa.Column('advanced_tongue_root', BOOLEAN, nullable=False, key=u'advanced_tongue_root', doc=''),
	sa.Column('less_rounded', BOOLEAN, nullable=False, key=u'less_rounded', doc=''),
	sa.Column('ejective', BOOLEAN, nullable=False, key=u'ejective', doc=''),
	sa.Column('mid_centralised', BOOLEAN, nullable=False, key=u'mid_centralised', doc=''),
	sa.Column('extra_short_length', BOOLEAN, nullable=False, key=u'extra_short_length', doc=''),
	sa.Column('high_falling_contour', BOOLEAN, nullable=False, key=u'high_falling_contour', doc=''),
	sa.Column('voiced', BOOLEAN, nullable=False, key=u'voiced', doc=''),
	sa.Column('centralised', BOOLEAN, nullable=False, key=u'centralised', doc=''),
	sa.Column('breathy_voiced', BOOLEAN, nullable=False, key=u'breathy_voiced', doc=''),
	sa.Column('rising_contour', BOOLEAN, nullable=False, key=u'rising_contour', doc=''),
	sa.Column('retracted', BOOLEAN, nullable=False, key=u'retracted', doc=''),
	sa.Column('retracted_tongue_root', BOOLEAN, nullable=False, key=u'retracted_tongue_root', doc=''),
	sa.Column('voiceless', BOOLEAN, nullable=False, key=u'voiceless', doc=''),
	sa.Column('palatalised', BOOLEAN, nullable=False, key=u'palatalised', doc=''),
	sa.Column('aspirated', BOOLEAN, nullable=False, key=u'aspirated', doc=''),
	sa.Column('nasalised', BOOLEAN, nullable=False, key=u'nasalised', doc=''),
	sa.Column('lateral_release', BOOLEAN, nullable=False, key=u'lateral_release', doc=''),
	sa.Column('low_falling_contour', BOOLEAN, nullable=False, key=u'low_falling_contour', doc=''),
	sa.Column('peaking_contour', BOOLEAN, nullable=False, key=u'peaking_contour', doc=''),
	sa.Column('syllabic', BOOLEAN, nullable=False, key=u'syllabic', doc=''),
	sa.Column('linguolabial', BOOLEAN, nullable=False, key=u'linguolabial', doc=''),
	sa.Column('velarised', BOOLEAN, nullable=False, key=u'velarised', doc=''),
	sa.Column('dipping_contour', BOOLEAN, nullable=False, key=u'dipping_contour', doc=''),
	sa.Column('downstep_tone', BOOLEAN, nullable=False, key=u'downstep_tone', doc=''),
	sa.Column('high_rising_contour', BOOLEAN, nullable=False, key=u'high_rising_contour', doc=''),
	sa.Column('pharyngealised', BOOLEAN, nullable=False, key=u'pharyngealised', doc=''),
	sa.Column('half_long_length', BOOLEAN, nullable=False, key=u'half_long_length', doc=''),
	sa.Column('falling_contour', BOOLEAN, nullable=False, key=u'falling_contour', doc=''),
	sa.Column('laminal', BOOLEAN, nullable=False, key=u'laminal', doc=''),
	sa.Column('long_length', BOOLEAN, nullable=False, key=u'long_length', doc=''),
	sa.Column('lowered', BOOLEAN, nullable=False, key=u'lowered', doc=''),
	sa.Column('low_rising_contour', BOOLEAN, nullable=False, key=u'low_rising_contour', doc=''),
	sa.Column('nasal_release', BOOLEAN, nullable=False, key=u'nasal_release', doc=''),
	sa.Column('advanced', BOOLEAN, nullable=False, key=u'advanced', doc=''),
	sa.Column('mid_tone', BOOLEAN, nullable=False, key=u'mid_tone', doc=''),
	sa.Column('apical', BOOLEAN, nullable=False, key=u'apical', doc=''),
	sa.Column('labialised', BOOLEAN, nullable=False, key=u'labialised', doc=''),
	sa.Column('dental', BOOLEAN, nullable=False, key=u'dental', doc=''),
	sa.Column('non_syllabic', BOOLEAN, nullable=False, key=u'non_syllabic', doc=''),
	sa.Column('rhotic', BOOLEAN, nullable=False, key=u'rhotic', doc=''),
	sa.Column('velarised_or_pharyngealised', BOOLEAN, nullable=False, key=u'velarised_or_pharyngealised', doc=''),
	sa.Column('high_tone', BOOLEAN, nullable=False, key=u'high_tone', doc=''),
	sa.Column('no_audible_release', BOOLEAN, nullable=False, key=u'no_audible_release', doc=''),
	sa.Column('upstep_tone', BOOLEAN, nullable=False, key=u'upstep_tone', doc=''),
	sa.Column('low_tone', BOOLEAN, nullable=False, key=u'low_tone', doc=''),
	sa.Column('creaky_voiced', BOOLEAN, nullable=False, key=u'creaky_voiced', doc=''),
	sa.Column('top_tone', BOOLEAN, nullable=False, key=u'top_tone', doc=''),
	sa.Column('prenasalised', BOOLEAN, nullable=False, key=u'prenasalised', doc=''),
)

t_suprasegmental_description = sa.Table('suprasegmental_description', metadata,
	sa.Column('ipa_id', TEXT, primary_key=True, key=u'appenKey', doc=''),
	sa.Column('global_fall', BOOLEAN, nullable=False, key=u'global_fall', doc=''),
	sa.Column('syllable_boundary', BOOLEAN, nullable=False, key=u'syllable_boundary', doc=''),
	sa.Column('morpheme_boundary', BOOLEAN, nullable=False, key=u'morpheme_boundary', doc=''),
	sa.Column('major_intonation_boundary', BOOLEAN, nullable=False, key=u'major_intonation_boundary', doc=''),
	sa.Column('minor_foot_boundary', BOOLEAN, nullable=False, key=u'minor_foot_boundary', doc=''),
	sa.Column('secondary_stress', BOOLEAN, nullable=False, key=u'secondary_stress', doc=''),
	sa.Column('primary_stress', BOOLEAN, nullable=False, key=u'primary_stress', doc=''),
	sa.Column('word_boundary', BOOLEAN, nullable=False, key=u'word_boundary', doc=''),
	sa.Column('linking', BOOLEAN, nullable=False, key=u'linking', doc=''),
	sa.Column('global_rise', BOOLEAN, nullable=False, key=u'global_rise', doc=''),
)

t_vowel_description = sa.Table('vowel_description', metadata,
	sa.Column('ipa_id', TEXT, primary_key=True, key=u'appenKey', doc=''),
	sa.Column('near_front', BOOLEAN, nullable=False, key=u'near_front', doc=''),
	sa.Column('near_open', BOOLEAN, nullable=False, key=u'near_open', doc=''),
	sa.Column('central', BOOLEAN, nullable=False, key=u'central', doc=''),
	sa.Column('near_close', BOOLEAN, nullable=False, key=u'near_close', doc=''),
	sa.Column('close', BOOLEAN, nullable=False, key=u'close', doc=''),
	sa.Column('near_back', BOOLEAN, nullable=False, key=u'near_back', doc=''),
	sa.Column('close_mid', BOOLEAN, nullable=False, key=u'close_mid', doc=''),
	sa.Column('back', BOOLEAN, nullable=False, key=u'back', doc=''),
	sa.Column('mid', BOOLEAN, nullable=False, key=u'mid', doc=''),
	sa.Column('unrounded', BOOLEAN, nullable=False, key=u'unrounded', doc=''),
	sa.Column('front', BOOLEAN, nullable=False, key=u'front', doc=''),
	sa.Column('rounded', BOOLEAN, nullable=False, key=u'rounded', doc=''),
	sa.Column('open', BOOLEAN, nullable=False, key=u'open', doc=''),
	sa.Column('open_mid', BOOLEAN, nullable=False, key=u'open_mid', doc=''),
)

t_payment_classes = sa.Table('payment_classes', metadata,
	sa.Column('payment_class_id', INTEGER, primary_key=True, autoincrement=False, key=u'paymentClassId', doc=''),
)

t_payrolls = sa.Table('payrolls', metadata,
	sa.Column('payroll_id', INTEGER, primary_key=True, autoincrement=False, key=u'payrollId', doc=''),
)

t_calculated_payments = sa.Table('calculated_payments', metadata,
	sa.Column('payment_id', INTEGER, primary_key=True, key=u'calculatedPaymentId', doc=''),
	sa.Column('payroll_id', INTEGER, sa.ForeignKey('payrolls.payrollId'), nullable=False, key=u'payrollId', doc=''),
	sa.Column('week_ending', DATE, nullable=False, key=u'weekEnding', doc=''),
	sa.Column('user_id', INTEGER, sa.ForeignKey('users.userId'), nullable=False, key=u'userId', doc=''),
	sa.Column('appenonline_task_id', INTEGER, nullable=False, key=u'appenonlineTaskId', doc=''),
	sa.Column('subtask_id', INTEGER, sa.ForeignKey('subtask.subTaskId'), nullable=False, key=u'subTaskId', doc=''),
	sa.Column('units', INTEGER, nullable=False, key=u'units', doc=''),
	sa.Column('original_amount', INTEGER, nullable=False, key=u'originalAmount', doc=''),
	sa.Column('amount', INTEGER, nullable=False, key=u'amount', doc=''),
	sa.Column('receipt', TEXT, key=u'receipt', doc=''),
	sa.Column('updated', BOOLEAN, nullable=False, key=u'updated', doc=''),
)

t_payable_events = sa.Table('payable_events', metadata,
	sa.Column('event_id', INTEGER, primary_key=True, autoincrement=True, key=u'eventId', doc=''),
	sa.Column('user_id', INTEGER, sa.ForeignKey('users.userId'), key=u'userId', doc=''),
	sa.Column('word_id', INTEGER, sa.ForeignKey('word.wordId'), key=u'wordId', doc=''),
	sa.Column('timestamp', TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'timestamp', doc=''),
	sa.Column('region_ratio', DOUBLE_PRECISION, key=u'regionalRatio', doc=''),
	sa.Column('user_group', INTEGER, key=u'userGroup', doc=''),
	sa.Column('user_payment_class', INTEGER, sa.ForeignKey('payment_classes.paymentClassId'), key=u'userPaymentClassId', doc=''),
	sa.Column('local_connection', BOOLEAN, key=u'localConnection', doc=''),
	sa.Column('subtask_id', INTEGER, sa.ForeignKey('subtask.subTaskId'), key=u'subTaskId', doc=''),
	sa.Column('expected_throughput', INTEGER, key=u'expectedThroughput', doc=''),
	sa.Column('base_pay_rate', INTEGER, key=u'basePayRate', doc=''),
	sa.Column('payment_id', INTEGER, sa.ForeignKey('calculated_payments.calculatedPaymentId'), key=u'calculatedPaymentId', doc=''),
)

t_page = sa.Table('page', metadata,
	sa.Column('page_id', INTEGER, primary_key=True, autoincrement=True, key=u'pageId', doc=''),
	sa.Column('page_name', TEXT, key=u'name', doc=''),
)

t_history = sa.Table('history', metadata,
	sa.Column('word_id', INTEGER, sa.ForeignKey('word.wordId'), nullable=False, key=u'wordId', doc=''),
	sa.Column('variant_number', INTEGER, nullable=False, key=u'ranking', doc=''),
	sa.Column('language_id', INTEGER, sa.ForeignKey('language.dialectId'), key=u'dialectId', doc=''),
	sa.Column('headword', TEXT, key=u'headword', doc=''),
	sa.Column('spelling_correction', TEXT, key=u'spellingCorrection', doc=''),
	sa.Column('transcription', TEXT, key=u'transcription', doc=''),
	sa.Column('comment', TEXT, key=u'comment', doc=''),
	sa.Column('subtask_id', INTEGER, sa.ForeignKey('subtask.subTaskId'), key=u'subTaskId', doc=''),
	sa.Column('user_id', INTEGER, key=u'userId', doc=''),
	sa.Column('timestamp', TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'timestamp', doc=''),
	sa.Column('alphabet_id', INTEGER, sa.ForeignKey('phonetic_alphabet.alphabetId'), nullable=False, key=u'alphabetId', doc=''),
	sa.Column('event_id', INTEGER, primary_key=True, key=u'eventId', doc=''),
	sa.Column('romanisation', TEXT, key=u'romanisation', doc=''),
)
sa.Index('history_subtask_user_timestamp', t_history.c.subTaskId, t_history.c.userId, t_history.c.timestamp, unique=False)
sa.Index('history_word_id', t_history.c.wordId, unique=False)

t_archived_history = sa.Table('archived_history', metadata,
	sa.Column('word_id', INTEGER, key=u'wordId', doc=''),
	sa.Column('variant_number', INTEGER, key=u'ranking', doc=''),
	sa.Column('language_id', INTEGER, key=u'dialectId', doc=''),
	sa.Column('headword', TEXT, key=u'headword', doc=''),
	sa.Column('spelling_correction', TEXT, key=u'spellingCorrection', doc=''),
	sa.Column('transcription', TEXT, key=u'transcription', doc=''),
	sa.Column('comment', TEXT, key=u'comment', doc=''),
	sa.Column('subtask_id', INTEGER, key=u'subTaskId', doc=''),
	sa.Column('user_id', INTEGER, key=u'userId', doc=''),
	sa.Column('timestamp', TIMESTAMP(timezone=True), key=u'timestamp', doc=''),
	sa.Column('alphabet_id', INTEGER, key=u'alphabetId', doc=''),
	sa.Column('event_id', INTEGER, key=u'eventId', doc=''),
	sa.Column('romanisation', TEXT, key=u'romanisation', doc=''),
	sa.PrimaryKeyConstraint(u'eventId'),
)
sa.Index('archived_history_subtask_user_timestamp', u'subTaskId', u'userId', u'timestamp', unique=False)
sa.Index('archived_history_word_id', u'wordId', unique=False)

t_archived_word_subtask_map = sa.Table('archived_word_subtask_map', metadata,
	sa.Column('subtask_id', INTEGER, key=u'subTaskId', doc=''),
	sa.Column('word_id', INTEGER, key=u'wordId', doc=''),
	sa.Column('variant_number', INTEGER, key=u'ranking', doc=''),
	sa.Column('user_id', INTEGER, key=u'userId', doc=''),
	sa.Column('timestamp', TIMESTAMP(timezone=True), key=u'timestamp', doc=''),
	sa.Column('expiry', TIMESTAMP(timezone=True), key=u'expiry', doc=''),
)
sa.Index('archived_word_subtask_map_subtask_id', u'subTaskId', unique=False)
sa.Index('archived_word_subtask_map_word_id', u'wordId', unique=False)

t_archived_word_task_map = sa.Table('archived_word_task_map', metadata,
	sa.Column('task_id', INTEGER, key=u'taskId', doc=''),
	sa.Column('variant_number', INTEGER, key=u'ranking', doc=''),
	sa.Column('word_id', INTEGER, key=u'wordId', doc=''),
)

t_user_page_modification_map = sa.Table('user_page_modification_map', metadata,
	sa.Column('user_id', INTEGER, sa.ForeignKey('users.userId'), nullable=False, key=u'userId', doc=''),
	sa.Column('page_id', INTEGER, sa.ForeignKey('page.pageId'), nullable=False, key=u'pageId', doc=''),
	sa.Column('alphabet_id', INTEGER, sa.ForeignKey('phonetic_alphabet.alphabetId'), nullable=False, key=u'alphabetId', doc=''),
	sa.Column('completion_count', INTEGER, key=u'completionCount', doc=''),
	sa.Column('timestamp', TIMESTAMP(timezone=True), key=u'timestamp', doc=''),
)

t_task_lexicon_import_map = sa.Table('task_lexicon_import_map', metadata,
	sa.Column('lexicon_import_id', INTEGER, primary_key=True, autoincrement=True, key=u'importId', doc=''),
	sa.Column('task_id', INTEGER, sa.ForeignKey('task.taskId'), nullable=False, key=u'taskId', doc=''),
	sa.Column('lexicon_import_date', TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'importedAt', doc=''),
	sa.Column('lexicon_import_filename', TEXT, nullable=False, key=u'filename', doc=''),
	sa.Column('lexicon_import_file', TEXT, nullable=False, key=u'data', doc=''),
)

t_task_lexicon_export_map = sa.Table('task_lexicon_export_map', metadata,
	sa.Column('lexicon_export_id', INTEGER, primary_key=True, autoincrement=True, key=u'exportId', doc=''),
	sa.Column('task_id', INTEGER, sa.ForeignKey('task.taskId'), nullable=False, key=u'taskId', doc=''),
	sa.Column('lexicon_export_date', TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'exportedAt', doc=''),
	sa.Column('lexicon_export_filename', TEXT, nullable=False, key=u'filename', doc=''),
	sa.Column('lexicon_export_file', TEXT, nullable=False, key=u'data', doc=''),
)


##########################################################################

# ISO 15924
t_writing_scripts = sa.Table('writingscripts', metadata,
	sa.Column('script_id', INTEGER, primary_key=True, autoincrement=True, key=u'scriptId', doc=''),
	sa.Column('name', TEXT, nullable=True, key=u'name', doc=''),
	sa.Column('code', VARCHAR(4), nullable=False, key=u'code', doc=''),
	sa.Column('n_code', VARCHAR(3), nullable=False, key=u'numericCode', doc=''),
	sa.UniqueConstraint(u'name'),
	sa.UniqueConstraint(u'code'),
	sa.UniqueConstraint(u'numericCode'),
	schema='dev',
)

t_dialects = sa.Table('dialects', metadata,
	sa.Column('dialect_id', INTEGER, primary_key=True, autoincrement=True, key=u'dialectId', doc=''),
	sa.Column('name', TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('language_code', CHAR(3), nullable=False, key=u'iso639_3', doc=''),
	sa.Column('country_code', CHAR(3), nullable=False, key=u'iso3166_3', doc=''),
	sa.Column('script_id', INTEGER, sa.ForeignKey('writingscripts.scriptId'), nullable=False, key=u'scriptId', doc=''),
	sa.Column('ltr', BOOLEAN, nullable=False, key=u'ltr', doc=''),
	sa.Column('romanization_scheme', TEXT, key=u'romanizationScheme', doc=''),
	schema='dev',
)

t_alphabets = sa.Table('alphabets', metadata,
	sa.Column('alphabet_id', INTEGER, primary_key=True, autoincrement=True, key=u'alphabetId', doc=''),
	sa.Column('name', TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('dialect_id', INTEGER, sa.ForeignKey('dev.dialects.dialectId'), nullable=False, key=u'dialectId', doc=''),
	sa.Column('active', BOOLEAN, nullable=False, server_default=sa.text('TRUE'), key=u'isActive', doc=''),
	sa.Column('manual_url', TEXT, key=u'url', doc=''),
	sa.UniqueConstraint(u'name'),
	schema='dev',
)

t_rules = sa.Table('rules', metadata,
	sa.Column('rule_id', INTEGER, primary_key=True, autoincrement=True, key=u'ruleId', doc=''),
	sa.Column('name', TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('type', TEXT, nullable=False, key=u'type', doc=''),
	sa.Column('description', TEXT, key=u'description', doc=''),
	sa.Column('alphabet_id', INTEGER, sa.ForeignKey('dev.alphabets.alphabetId'), nullable=False, key=u'alphabetId', doc=''),
	sa.UniqueConstraint(u'name', u'alphabetId'),
	sa.CheckConstraint("type=ANY(ARRAY['phonology','stress','syllabification','vowelisation'])"),
	schema='dev',
)

t_graphemes = sa.Table('graphemes', metadata,
	sa.Column('grapheme_id', INTEGER, primary_key=True, autoincrement=True, key=u'graphemeId', doc=''),
	sa.Column('key', TEXT, nullable=False, key=u'key', doc=''),
	sa.Column('alphabet_id', INTEGER, sa.ForeignKey('dev.alphabets.alphabetId'), nullable=False, key=u'alphabetId', doc=''),
	sa.Column('token', TEXT, nullable=False, key=u'token', doc=''),
	sa.Column('orthography', TEXT, key=u'orthography', doc=''),
	sa.Column('romanization', TEXT, key=u'romanization', doc=''),
	sa.Column('sample_word', TEXT, key=u'sampleWord', doc=''),
	sa.Column('sample_transcription', TEXT, key=u'sampleTranscription', doc=''),
	sa.Column('sample_romanization', TEXT, key=u'sampleRomanization', doc=''),
	sa.UniqueConstraint(u'alphabetId', u'key'),
	sa.UniqueConstraint(u'alphabetId', u'token'),
	schema='dev',
)


t_rawpieces = sa.Table('rawpieces', metadata,
	sa.Column(u'rawpieceid', INTEGER, primary_key=True, nullable=False, key=u'rawPieceId', doc=''),
	sa.Column(u'taskid', INTEGER, nullable=False, key=u'taskId', doc=''),
	sa.Column(u'rawtext', TEXT, key=u'rawText', doc=''),
	sa.Column(u'assemblycontext', TEXT, nullable=False, key=u'assemblyContext', doc=''),
	sa.Column(u'allocationcontext', TEXT, nullable=False, key=u'allocationContext', doc=''),
	sa.Column(u'meta', TEXT, key=u'meta', doc=''),
	sa.Column(u'isnew', BOOLEAN, nullable=False, server_default=sa.text(u'true'), key=u'isNew', doc=''),
	sa.Column(u'hypothesis', TEXT, key=u'hypothesis', doc=''),
	sa.Column(u'words', INTEGER, server_default=sa.text(u'0'), key=u'words', doc=''),
	sa.Column(u'groupid', INTEGER, key=u'groupId', doc=''),
	sa.Column(u'loadid', INTEGER, key=u'loadId', doc=''),
	sa.UniqueConstraint(u'taskId', u'assemblyContext'),
	# sa.ForeignKeyConstraint([u'taskId'], [u'tasks.taskId']),
	# sa.ForeignKeyConstraint([u'groupId'], [u'postprocessingutterancegroups.groupId']),
	# sa.ForeignKeyConstraint([u'taskId', u'loadId'], [u'loads.taskId', u'loads.loadId']),
	schema='dev',
)


t_loads = sa.Table('loads', metadata,
	sa.Column(u'loadid', INTEGER, primary_key=True, nullable=False, key=u'loadId', doc=''),
	sa.Column(u'createdby', INTEGER, nullable=False, key=u'createdBy', doc=''),
	sa.Column(u'createdat', TIMESTAMP(timezone=True), nullable=False, server_default=sa.text(u'now()'), key=u'createdAt', doc=''),
	sa.Column(u'taskid', INTEGER, nullable=False, key=u'taskId', doc=''),
	# sa.ForeignKeyConstraint([u'createdBy'], [u'users.userId']),
	# sa.ForeignKeyConstraint([u'taskId'], [u'tasks.taskId']),
	schema='dev',
)
# Index('ix_loads_taskid_loadid', t_loads.c.loadId, t_loads.c.taskId, unique=True)


##########################################################################

__all__ = [name for name in locals().keys()
		if name.startswith('t_') or name.startswith('j_')]
__all__.insert(0, 'metadata')
