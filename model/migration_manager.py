import sys
import os.path
from model.card_generators.times_table_generator import TimesTableGenerator
from model.card_generators.notes_generator import NotesGenerator
from model.card_generators.intervals_generator import IntervalsGenerator
from model.card_generators.chords_generator import ChordsGenerator

class MigrationManager:
	@staticmethod
	def create_db(db):
		with open('model/schema.sql') as f:
			db.execute_statments(f.read().split(';'))

	@staticmethod
	def insert_times_tables(db):
		cards = TimesTableGenerator.generate_cards()
		db.execute_statments([
			""" INSERT INTO Deck (name, descr) VALUES ('Times Tables', 'Ex: 1* 1')"""
		])
		deck_id = db.select1(table="Deck", where="name='Times Tables'", columns="deck_id")[0]
		for c in cards: c['deck_id'] = deck_id
		db.insert_key_value_pairs('Card', cards)

	@staticmethod
	def insert_notes_cards(db):
		cards = NotesGenerator.generate_cards()
		db.execute_statments([
			""" INSERT INTO Deck (name, descr) VALUES ('Notes', 'Uses graphics')"""
		])
		deck_id = db.select1(table="Deck", where="name='Notes'", columns="deck_id")[0]
		for c in cards: c['deck_id'] = deck_id
		db.insert_key_value_pairs('Card', cards)

	@staticmethod
	def insert_intervals_cards(db):
		cards = IntervalsGenerator.generate_cards()
		db.execute_statments([
			""" INSERT INTO Deck (name, descr, answer_validator) 
				VALUES ('Intervals', 'Interval math!', 'answerValidator_multipleOptions_equals')"""
		])
		deck_id = db.select1(table="Deck", where="name='Intervals'", columns="deck_id")[0]
		for c in cards: c['deck_id'] = deck_id
		db.insert_key_value_pairs('Card', cards)

	@staticmethod
	def insert_major_chords_cards(db):
		cards = ChordsGenerator.generate_major_chord_cards()
		db.execute_statments([
			""" INSERT INTO Deck (name, descr, answer_validator) 
				VALUES ('Major Chords', 'Major chords in all inversions', 'answerValidator_equals_midiEnharmonicsValid')"""
		])
		deck_id = db.select1(table="Deck", where="name='Major Chords'", columns="deck_id")['deck_id']
		for c in cards: c['deck_id'] = deck_id
		db.insert_key_value_pairs('Card', cards)

	@staticmethod
	def insert_minor_chords_cards(db):
		cards = ChordsGenerator.generate_minor_chord_cards()
		db.execute_statments([
			""" INSERT INTO Deck (name, descr, answer_validator) 
				VALUES ('Minor Chords', 'Minor chords in all inversions', 'answerValidator_equals_midiEnharmonicsValid')"""
		])
		deck_id = db.select1(table="Deck", where="name='Minor Chords'", columns="deck_id")['deck_id']
		for c in cards: c['deck_id'] = deck_id
		db.insert_key_value_pairs('Card', cards)

	@staticmethod
	def insert_major_and_minor_chords_cards(db):
		cards = ChordsGenerator.generate_major_and_minor_chord_cards()
		db.execute_statments([
			""" INSERT INTO Deck (name, descr, answer_validator) 
				VALUES ('Major and Minor Chords', 'Major and Minor chords in all inversions', 'answerValidator_equals_midiEnharmonicsValid')"""
		])
		deck_id = db.select1(table="Deck", where="name='Major and Minor Chords'", columns="deck_id")['deck_id']
		for c in cards: c['deck_id'] = deck_id
		db.insert_key_value_pairs('Card', cards)

	@staticmethod
	def insert_all_pregenerated_decks_and_create_db(db):
		MigrationManager.create_db(db)
		MigrationManager.insert_times_tables(db)
		MigrationManager.insert_notes_cards(db)
		MigrationManager.insert_intervals_cards(db)
		MigrationManager.insert_major_chords_cards(db)
		MigrationManager.insert_minor_chords_cards(db)
		MigrationManager.insert_major_and_minor_chords_cards(db)