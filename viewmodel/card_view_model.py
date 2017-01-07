from model.db import db
from model.objects.card import Card

class CardViewModel:
	@staticmethod
	def all_cards_from_deck(deck_id):
		cards = db.select(table="Card", where="deck_id = {}".format(deck_id))
		return map(lambda f: Card(f[0], f[1], f[2], f[3]), cards)

		