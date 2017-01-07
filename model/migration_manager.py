import sys
import os.path
from model.card_generators.times_table_generator import TimesTableGenerator
from model.card_generators.notes_generator import NotesGenerator
from model.card_generators.intervals_generator import IntervalsGenerator

class MigrationManager:
	@staticmethod
	def create_db(db):
		sql = """
			CREATE TABLE Deck (
			    deck_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
			    name VARCHAR(100) NOT NULL, 
			    descr VARCHAR(500),
			    answer_validator VARCHAR(256)
			);

			CREATE TABLE Card (
			    card_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
			    deck_id INTEGER NOT NULL, 
			    question VARCHAR(2000) NOT NULL,  
			    answer VARCHAR(2000) NOT NULL
			);

			CREATE TABLE Session (
			    session_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
			    deck_id INTEGER NOT NULL, 
			    begin_date DATETIME NOT NULL, 
			    end_date DATETIME,
			    median DOUBLE
			);

			CREATE TABLE AnswerHistory (
			    answer_history_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
			    session_id INTEGER NOT NULL, 
			    card_id INTEGER NOT NULL, 
			    time_to_correct DOUBLE NOT NULL, 
			    first_attempt_correct BOOLEAN NOT NULL, 
			    answered_at DATETIME NOT NULL
			);

			CREATE TABLE SessionCard (
			    session_card_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
			    session_id INTEGER NOT NULL,
			    card_id INTEGER NOT NULL
			);
		"""

		db.execute_statments(sql.split(';'))

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
		# db.select(table='Card', debug=True)

	@staticmethod
	def insert_all_pregenerated_decks_and_create_db(db):
		MigrationManager.create_db(db)
		MigrationManager.insert_times_tables(db)
		MigrationManager.insert_notes_cards(db)
		MigrationManager.insert_intervals_cards(db)

