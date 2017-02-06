from model.card_generators.times_table_generator import TimesTableGenerator
from model.card_generators.notes_generator import NotesGenerator
from model.card_generators.intervals_generator import IntervalsGenerator
from model.card_generators.chords_generator import ChordsGenerator
from model.card_generators.progression_generator import ProgressionGenerator
from model.db import db

def insert_deck(db, deck_name, deck_desc, cards):
	db.execute(
		""" INSERT INTO Deck (name, descr) VALUES (?, ?)""",
		(deck_name, deck_desc)
	)
	deck_id = db.select1(table="Deck", where="name = ?", substitutions=(deck_name,))['deck_id']
	for c in cards: c['deck_id'] = deck_id
	db.insert_key_value_pairs('Card', cards)

insert_deck(
	db, 
	"Notes", 
	"On the staff", 
	NotesGenerator.generate_cards()
)

insert_deck(
	db, 
	"Intervals", 
	"Interval math!", 
	IntervalsGenerator.generate_cards()
)

insert_deck(
	db, 
	'Major Chords', 
	'Major chords in all inversions', 
	ChordsGenerator.generate_major_chord_cards()
)

insert_deck(
	db, 
	'Minor Chords', 
	'Minor chords in all inversions', 
	ChordsGenerator.generate_minor_chord_cards()
)

insert_deck(
	db, 
	'Diminished Chords', 
	'Diminished chords in all inversions', 
	ChordsGenerator.generate_dim_chords_cards()
)

insert_deck(
	db, 
	'Major and Minor Chords', 
	'Major and Minor chords in all inversions', 
	ChordsGenerator.generate_major_and_minor_chord_cards()
)

insert_deck(
	db, 
	'IV V I Cadence', 
	'Includes common sets of inversions', 
	ProgressionGenerator.four_five_one_cards()
)
