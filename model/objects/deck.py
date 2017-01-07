from model.db import db
from model.objects.card import Card

class Deck:
	@staticmethod
	def from_deck_id(deck_id):
		return Deck.from_db(db.select1(table="Deck", where="deck_id = {}".format(deck_id)))

	@staticmethod
	def from_db(row):
		return Deck(row[0], row[1], row[2], row[3])

	def __init__(self, deck_id, name, descr, answer_validator):
		self.deck_id = deck_id
		self.name = name
		self.descr = descr
		if answer_validator:
			self.answer_validator = answer_validator 
		else:
			self.answer_validator = "answerValidator_multipleOptions_equals" 

	def load_cards(self):
		rows = db.select(table="Card", where="deck_id = {}".format(self.deck_id))
		self.cards = list(map(lambda c: Card.from_db(c), rows))
		