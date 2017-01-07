from model.db import db
from model.objects.deck import Deck

class DeckViewModel:
	@staticmethod
	def all_decks():
		decks = db.select("Deck")
		decks = map(lambda d: Deck.from_db(d), decks)
		return list(decks)

