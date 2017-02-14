from model.card_generators.chords_generator import ChordsGenerator
from model.db import db

def update_deck(db, deck_name, cards):
	deck_id = db.select1(table="Deck", where="name = ?", substitutions=(deck_name,))['deck_id']
	for c in cards: 
		card_id = db.select1(
			table="Card", 
			where="template_data = ? and answer = ?", 
			substitutions=(c['template_data'], c['answer'])
		)['card_id']
		db.execute("""
			UPDATE Card SET accidental = ? WHERE card_id = ?
		""", substitutions=(c['accidental'], card_id))

update_deck(
	db, 
	'Major Triads', 
	ChordsGenerator.generate_major_chord_cards()
)

update_deck(
	db, 
	'Minor Triads', 
	ChordsGenerator.generate_minor_chord_cards()
)

