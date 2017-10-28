from model.card_generators.notes_generator import NotesGenerator
from model.objects.user import User

if User.from_email('rednebmas@gmail.com') is None:
	User.create('sam', 'rednebmas@gmail.com', 'sam')

# i should make sure this insert_deck function is scoped properly (defined in first migration)
insert_deck(
	db, 
	"Notes", 
	"On the staff", 
	NotesGenerator.generate_cards()
)