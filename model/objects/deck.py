from model.db import db
from model.objects.card import Card

class Deck:
	@staticmethod
	def from_deck_id(deck_id):
		return Deck.from_db(db.select1(table="Deck", where="deck_id = {}".format(deck_id)))

	@staticmethod
	def from_db(row):
		return Deck(row['deck_id'], row['name'], row['descr'])

	def __init__(self, deck_id, name, descr):
		self.deck_id = deck_id
		self.name = name
		self.descr = descr

	def load_cards(self):
		rows = db.select(table="Card", where="deck_id = {}".format(self.deck_id))
		self.cards = list(map(lambda c: Card.from_db(c), rows))

	@staticmethod
	def unseen_cards(session):
		sql = """
		SELECT C.*, AH.answer_history_id
		FROM Card C
		LEFT JOIN AnswerHistory AH ON C.card_id = AH.card_id
		WHERE C.deck_id = ?
			  AND AH.answer_history_id IS NULL
		GROUP BY C.card_id
		ORDER BY C.card_id
		"""
		db.execute(sql, (session.deck_id,))
		rows = db.cursor.fetchall()
		return list(map(lambda r: Card.from_db(r), rows))


		