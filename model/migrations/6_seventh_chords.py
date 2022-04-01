from model.card_generators.chords_generator import ChordsGenerator
from model.objects.user import User
import random

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
	"Dominant 7th Chords", 
	"Oh, the tension!", 
	ChordsGenerator.generate_dom7_chords_cards()
)

row = db.select1("Deck", "name = 'Dominant 7th Chords'")
row_id = row['deck_id']
db.execute("INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, ?), (2, ?), (3, ?)", (row_id, row_id, row_id))


insert_deck(
	db, 
	"Minor 7th Chords", 
	"Scary!", 
	ChordsGenerator.generate_min7_chords_cards()
)

row = db.select1("Deck", "name = 'Minor 7th Chords'")
row_id = row['deck_id']
db.execute("INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, ?), (2, ?), (3, ?)", (row_id, row_id, row_id))


insert_deck(
	db, 
	"Major 7th Chords", 
	"", 
	ChordsGenerator.generate_min7_chords_cards()
)

row = db.select1("Deck", "name = 'Major 7th Chords'")
row_id = row['deck_id']
db.execute("INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, ?), (2, ?), (3, ?)", (row_id, row_id, row_id))


insert_deck(
	db, 
	"m7b5 Chords", 
	"", 
	ChordsGenerator.generate_m7b5_chords_cards()
)

row = db.select1("Deck", "name = 'm7b5 Chords'")
row_id = row['deck_id']
db.execute("INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, ?), (2, ?), (3, ?)", (row_id, row_id, row_id))

insert_deck(
	db, 
	"dim7 Chords", 
	"", 
	ChordsGenerator.generate_dim7_chords_cards()
)

row = db.select1("Deck", "name = 'dim7 Chords'")
row_id = row['deck_id']
db.execute("INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, ?), (2, ?), (3, ?)", (row_id, row_id, row_id))


insert_deck(
	db, 
	"Minor Major 7th Chords", 
	"Also known as the Hitchcock Chord", 
	ChordsGenerator.generate_min_maj7_chords_cards()
)

row = db.select1("Deck", "name = 'Minor Major 7th Chords'")
row_id = row['deck_id']
db.execute("INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, ?), (2, ?), (3, ?)", (row_id, row_id, row_id))

all_chords = ChordsGenerator.generate_dom7_chords_cards()
all_chords += ChordsGenerator.generate_min7_chords_cards()
all_chords += ChordsGenerator.generate_maj7_chords_cards()
all_chords += ChordsGenerator.generate_m7b5_chords_cards()
all_chords += ChordsGenerator.generate_dim7_chords_cards()
all_chords += ChordsGenerator.generate_min_maj7_chords_cards()
random.shuffle(all_chords)

insert_deck(
	db, 
	"All 7th Chords", 
	"", 
	all_chords
)

row = db.select1("Deck", "name = 'All 7th Chords'")
row_id = row['deck_id']
db.execute("INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, ?), (2, ?), (3, ?)", (row_id, row_id, row_id))