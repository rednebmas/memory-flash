import math
from model.db import db, DB
from model.objects.deck import Deck
from model.objects.card import Card
from model.objects.answer_history import AnswerHistory
from model.math_sam import choose_index_for_weights

class Session:
	@staticmethod
	def from_deck_id(deck_id, user_id):
		rows = db.select(
			table="Session", 
			where="user_id = ? AND deck_id = ? AND stage <> 'finished'", 
			substitutions=(user_id, deck_id), 
			limit="1", 
			order_by="begin_date DESC"
		)
		if len(rows) == 0:
			return Session.new_for_deck_id(deck_id, user_id)
		else:
			return Session.from_db(rows[0])

	@staticmethod
	def from_db_id(session_id):
		try:
			row = db.select1(table="Session", where="session_id = ?", substitutions=(session_id,))
			return Session.from_db(row)
		except Exception as e:
			return None

	@staticmethod
	def new_for_deck_id(deck_id, user_id):
		db.execute('INSERT INTO Session (user_id, deck_id, begin_date) VALUES (?, ?, ?)', (user_id, deck_id, DB.datetime_now()))
		row = db.select1(table="Session", where="user_id = ? AND deck_id = ?", order_by="session_id DESC", substitutions=(user_id, deck_id))
		return Session.from_db(row)

	@staticmethod
	def from_db(row):
		return Session(row['session_id'], row['deck_id'], row['user_id'], row['begin_date'], row['stage'], row['median'] if 'median' in row.keys() else None)

	def __init__(self, session_id, deck_id, user_id, begin_date, stage, median=None):
		self.session_id = session_id
		self.deck_id = deck_id
		self.user_id = user_id
		self.begin_date = begin_date
		self.stage = stage
		self.median = median
		self.cards_loaded = False

	def add_seen_cards(self):
		self.load_cards()

		unseen_cards = Deck.unseen_cards(self)
		seen_cards = AnswerHistory.first_review_from_last_day_reviewed_not_in_session(self)
		seen_cards_weights = [r['time_to_correct'] for r in seen_cards]
		num_seen_cards = len(seen_cards)

		# unseen cards still left in deck and this isn't the first session of the deck, because there will be no seen cards at that point
		if len(unseen_cards) != 0 and len(seen_cards): 
			num_seen_cards_to_add_to_deck = int(len(self.cards) * (1/3))
			card_ids_to_add = []
			print('len of seen_cards: ' + str(len(seen_cards)) + ', add_to_deck_#: ' + str(num_seen_cards_to_add_to_deck))
			for i in range(num_seen_cards_to_add_to_deck):
				pick_index = choose_index_for_weights(seen_cards_weights, 2.5)
				print('pick index1: ' + str(pick_index))
				card_ids_to_add.append(seen_cards[pick_index]['card_id'])
				del seen_cards[pick_index]
				del seen_cards_weights[pick_index]
			self.add_cards_to_session_deck(card_ids_to_add)
		elif len(unseen_cards) == 0: # no unseen cards left in deck
			cards_to_add_ids = []
			cards_to_add_time_to_corrects = []
			while (sum(cards_to_add_time_to_corrects) < 60.0 or len(cards_to_add_ids) < 8) or len(cards_to_add_ids) == num_seen_cards:
				pick_index = choose_index_for_weights(seen_cards_weights, 2.8)
				cards_to_add_ids.append(seen_cards[pick_index]['card_id'])
				cards_to_add_time_to_corrects.append(seen_cards[pick_index]['time_to_correct'])
				del seen_cards[pick_index]
				del seen_cards_weights[pick_index]
			print('stopped adding seen cards with sum: ' + str(sum(cards_to_add_time_to_corrects)))
			self.add_cards_to_session_deck(cards_to_add_ids)

		self.load_cards()

	def add_cards_to_session_deck(self, card_ids):
		for card_id in card_ids:
			print('adding card with id to session: ' + str(card_id))
			db.execute("""
				INSERT INTO SessionCard (session_id, card_id, user_id)
				VALUES (?, ?, ?)
				""",
				substitutions=(self.session_id, card_id, self.user_id)
			)

	def update_median(self):
		if self.cards_loaded == False: self.load_cards()
		time_to_correct_list = sorted([card.answer_history.time_to_correct for card in self.cards])
		self.median = time_to_correct_list[int(len(self.cards) / 2)]
		db.execute("UPDATE Session SET median = ? WHERE session_id = ?",  (self.median, self.session_id))

	def load_cards(self):
		statement = r"""
			SELECT Card.*,
				   AnswerHistory.time_to_correct, 
				   AnswerHistory.first_attempt_correct, 
				   MAX(AnswerHistory.answered_at) as answered_at
			FROM SessionCard
			JOIN Card on Card.card_id = SessionCard.card_id
			LEFT JOIN AnswerHistory on SessionCard.card_id = AnswerHistory.card_id
			WHERE SessionCard.session_id = ? AND SessionCard.user_id = ?
			GROUP BY SessionCard.card_id, SessionCard.session_id
		"""

		db.execute(statement, (self.session_id, self.user_id))
		rows = db.cursor.fetchall()

		self.cards = []
		for row in rows:
			card = Card.from_db(row)
			answer_history = AnswerHistory(
				session_id = self.session_id, 
				card_id = card.card_id, 
				user_id = self.user_id,
				time_to_correct = row['time_to_correct'], 
				first_attempt_correct = row['first_attempt_correct'], 
				answered_at = row['answered_at']
			)
			card.set_answer_history(answer_history)
			self.cards.append(card)

		self.cards_loaded = True

	def update_stage(self, new_val):
		statement = """UPDATE Session SET stage = ? WHERE session_id = ?"""
		db.execute(statement, substitutions=(new_val, self.session_id,))
		self.stage = new_val

