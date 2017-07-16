from model.db import db
from model.objects.card import Card
from model.objects.input_modality import InputModality

class Deck:
	@staticmethod
	def from_id(deck_id):
		return Deck.from_db(db.select1(table="Deck", where="deck_id = {}".format(deck_id)))

	@staticmethod
	def from_db(row):
		return Deck(row['deck_id'], row['name'], row['descr'])

	def __init__(self, deck_id, name, descr):
		self.deck_id = deck_id
		self.name = name
		self.descr = descr

	def load_cards(self):
		rows = db.select(table="Card", where="deck_id = ?", substitutions=(self.deck_id,))
		self.cards = list(map(lambda c: Card.from_db(c), rows))

	def input_modalities(self):
		sql = """
		SELECT IM.input_modality_id, IM.input_modality_name
		FROM InputModality IM
		JOIN DeckInputModality DIM ON DIM.input_modality_id = IM.input_modality_id
		WHERE DIM.deck_id = ?
		ORDER BY IM.input_modality_id
		"""
		db.execute(sql, (self.deck_id,))
		rows = db.cursor.fetchall()
		return list(map(lambda r: InputModality.from_db(r), rows))

	@staticmethod
	def unseen_cards(session):
		sql = """
		SELECT C.*, AH.answer_history_id
		FROM Card C
		LEFT JOIN AnswerHistory AH ON C.card_id = AH.card_id
		LEFT JOIN Session S ON AH.session_id = S.session_id
		WHERE C.deck_id = ?
			  AND (S.input_modality_id = ? OR S.input_modality_id IS NULL)
			  AND AH.answer_history_id IS NULL
			  -- This enforces the user_id isn't someone elses, it will never be the session's
			  -- user_id
			  AND (AH.user_id = ? OR AH.user_id IS NULL) 
		GROUP BY C.card_id
		ORDER BY C.card_id
		"""
		db.execute(sql, (session.deck_id, session.input_modality_id, session.user_id))
		rows = db.cursor.fetchall()
		return list(map(lambda r: Card.from_db(r), rows))
