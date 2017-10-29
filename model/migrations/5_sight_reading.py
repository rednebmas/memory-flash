from model.card_generators.notes_generator import NotesGenerator
from model.objects.user import User

if User.from_email('rednebmas@gmail.com') is None:
	User.create('sam', 'rednebmas@gmail.com', 'sam')

# i should make sure this insert_deck function is scoped properly (defined in first migration)
# treble clef
insert_deck(
	db, 
	"Treble Clef", 
	"On the staff", 
	NotesGenerator.treble_cards()
)

treble_clef_row = db.select1("Deck", "name = 'Treble Clef'")
treble_clef_id = treble_clef_row['deck_id']
db.execute("INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, ?), (3, ?)", (treble_clef_id, treble_clef_id))

# bass clef
insert_deck(
	db, 
	"Bass Clef", 
	"On the staff", 
	NotesGenerator.bass_cards()
)

bass_clef_row = db.select1("Deck", "name = 'Bass Clef'")
bass_clef_id = bass_clef_row['deck_id']
db.execute("INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, ?), (2, ?)", (bass_clef_id, bass_clef_id))

