import math
from model.db import db, DB
from model.objects.card import Card
from model.objects.answer_history import AnswerHistory

class Session:
	@staticmethod
	def from_deck_id(deck_id):
		rows = db.select(table="Session", where="deck_id = {}".format(deck_id), limit="1", order_by="begin_date DESC")
		if len(rows) == 0:
			return Session.new_for_deck_id(deck_id)
		else:
			return Session.from_db(rows[0])

	@staticmethod
	def new_for_deck_id(deck_id):
		db.execute('INSERT INTO Session (deck_id, begin_date) VALUES (?, ?)', (deck_id, DB.datetime_now()))
		row = db.select1(table="Session", where="deck_id = ?", order_by="begin_date DESC", substitutions=(deck_id,))
		return Session.from_db(row)

	@staticmethod
	def from_db(row):
		return Session(row[0], row[1], row[2], row[3], row[4])

	def __init__(self, session_id, deck_id, begin_date, end_date, median):
		self.session_id = session_id
		self.deck_id = deck_id
		self.begin_date = begin_date
		self.end_date = end_date
		self.median = median
		self.cards_loaded = False

	def is_fully_initialized(self):
		""" False means we have not calculated the median and added cards that we have already seen. """
		return self.median is None

	def fully_initialize(self):
		self.put_median_in_db()


	def load_cards(self):
		statement = r"""
			SELECT Card.*,
				   AnswerHistory.time_to_correct, 
				   AnswerHistory.first_attempt_correct, 
				   MAX(AnswerHistory.answered_at) as answered_at
			FROM AnswerHistory
			JOIN Card ON Card.card_id = AnswerHistory.card_id
			JOIN SessionCard ON SessionCard.card_id = Card.card_id and SessionCard.session_id = ?
			WHERE SessionCard.session_id = ?
			GROUP BY AnswerHistory.card_id
		"""

		db.execute(statement, (self.session_id, self.session_id))
		rows = db.cursor.fetchall()

		self.cards = []
		for row in rows:
			card = Card.from_db(row)
			answer_history = AnswerHistory(
				session_id = self.session_id, 
				card_id = card.card_id, 
				time_to_correct = row['time_to_correct'], 
				first_attempt_correct = row['first_attempt_correct'], 
				answered_at = row['answered_at']
			)
			card.set_answer_history(answer_history)
			self.cards.append(card)

		self.cards_loaded = True

	def put_median_in_db(self):
		if self.cards_loaded == False: self.load_cards()
		time_to_correct_list = sorted([card.answer_history.time_to_correct for card in self.cards])
		self.median = time_to_correct_list[int(len(self.cards) / 2)]
		conn = db.conn()
		cursor = conn.cursor()
		cursor.execute(r"""UPDATE Session SET median=? WHERE session_id = ?""", (self.median, self.session_id))
		db.commit()


