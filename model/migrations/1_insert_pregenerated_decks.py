from model.card_generators.times_table_generator import TimesTableGenerator
from model.card_generators.notes_generator import NotesGenerator
from model.card_generators.intervals_generator import IntervalsGenerator
from model.card_generators.chords_generator import ChordsGenerator
from model.card_generators.progression_generator import ProgressionGenerator

def insert_notes_cards(db):
	cards = NotesGenerator.generate_cards()
	db.execute_statments([
		""" INSERT INTO Deck (name, descr) VALUES ('Notes', 'Uses graphics')"""
	])
	deck_id = db.select1(table="Deck", where="name='Notes'", columns="deck_id")[0]
	for c in cards: c['deck_id'] = deck_id
	db.insert_key_value_pairs('Card', cards)

def insert_intervals_cards(db):
	cards = IntervalsGenerator.generate_cards()
	db.execute_statments([
		""" INSERT INTO Deck (name, descr, answer_validator) 
			VALUES ('Intervals', 'Interval math!', 'answerValidator_multipleOptions_equals')"""
	])
	deck_id = db.select1(table="Deck", where="name='Intervals'", columns="deck_id")[0]
	for c in cards: c['deck_id'] = deck_id
	db.insert_key_value_pairs('Card', cards)

def insert_major_chords_cards(db):
	cards = ChordsGenerator.generate_major_chord_cards()
	db.execute_statments([
		""" INSERT INTO Deck (name, descr, answer_validator) 
			VALUES ('Major Chords', 'Major chords in all inversions', 'answerValidator_equals_midiEnharmonicsValid')"""
	])
	deck_id = db.select1(table="Deck", where="name='Major Chords'", columns="deck_id")['deck_id']
	for c in cards: c['deck_id'] = deck_id
	db.insert_key_value_pairs('Card', cards)

def insert_minor_chords_cards(db):
	cards = ChordsGenerator.generate_minor_chord_cards()
	db.execute_statments([
		""" INSERT INTO Deck (name, descr, answer_validator) 
			VALUES ('Minor Chords', 'Minor chords in all inversions', 'answerValidator_equals_midiEnharmonicsValid')"""
	])
	deck_id = db.select1(table="Deck", where="name='Minor Chords'", columns="deck_id")['deck_id']
	for c in cards: c['deck_id'] = deck_id
	db.insert_key_value_pairs('Card', cards)

def insert_diminished_chords_cards(db):
	cards = ChordsGenerator.generate_dim_chords_cards()
	db.execute_statments([
		""" INSERT INTO Deck (name, descr, answer_validator) 
			VALUES ('Diminished Chords', 'Diminished chords in all inversions', 'answerValidator_equals_midiEnharmonicsValid')"""
	])
	deck_id = db.select1(table="Deck", where="name='Diminished Chords'", columns="deck_id")['deck_id']
	for c in cards: c['deck_id'] = deck_id
	db.insert_key_value_pairs('Card', cards)

def insert_major_and_minor_chords_cards(db):
	cards = ChordsGenerator.generate_major_and_minor_chord_cards()
	db.execute_statments([
		""" INSERT INTO Deck (name, descr, answer_validator) 
			VALUES ('Major and Minor Chords', 'Major and Minor chords in all inversions', 'answerValidator_equals_midiEnharmonicsValid')"""
	])
	deck_id = db.select1(table="Deck", where="name='Major and Minor Chords'", columns="deck_id")['deck_id']
	for c in cards: c['deck_id'] = deck_id
	db.insert_key_value_pairs('Card', cards)

def insert_four_five_one_cadence(db):
	cards = ProgressionGenerator.four_five_one_cards()
	db.execute_statments([
		""" INSERT INTO Deck (name, descr, answer_validator) 
			VALUES ('IV V I Cadence', 'Includes common sets of inversions', 'answerValidator_equals_midiEnharmonicsValid')"""
	])
	deck_id = db.select1(table="Deck", where="name='IV V I Cadence'", columns="deck_id")['deck_id']
	for c in cards: c['deck_id'] = deck_id
	db.insert_key_value_pairs('Card', cards)

# the meat
from model.db import db
insert_notes_cards(db)
insert_intervals_cards(db)
insert_major_chords_cards(db)
insert_minor_chords_cards(db)
insert_major_and_minor_chords_cards(db)
insert_four_five_one_cadence(db)
