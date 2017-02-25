from model.db import db, DB

class AnswerHistory:
	@staticmethod
	def from_json(json):
		return AnswerHistory(
			json['session_id'], 
			json['card_id'], 
			json['time_to_correct'], 
			json['first_attempt_correct'], 
			json['answered_at'] if 'answered_at' in json else DB.datetime_now()
		) 

	def __init__(self, session_id, card_id, time_to_correct, first_attempt_correct, answered_at):
		self.session_id = session_id
		self.card_id = card_id
		self.time_to_correct = time_to_correct
		self.first_attempt_correct = first_attempt_correct
		self.answered_at = answered_at

	def __str__(self):
		return "Time to correct: {}".format(self.time_to_correct)

	def insert(self):
		db.execute("""
			INSERT INTO AnswerHistory (session_id, card_id, time_to_correct, first_attempt_correct, answered_at, answered_at_day)
			VALUES (?, ?, ?, ?, ?, ?)
		 	""", (self.session_id, 
		 	   self.card_id, 
		 	   self.time_to_correct if self.time_to_correct < 45.0 else 45.0, 
		 	   self.first_attempt_correct,
		 	   self.answered_at,
		 	   self.answered_at[0:10],
		 	   )
		)

		# put into SessionCard if it doesn't already exist
		# to do this we must first check if it is in SessionCard
		count = db.select1(
			table="SessionCard",
			columns="COUNT(*)",
			where="session_id = ? AND card_id = ?",
			substitutions=(self.session_id, self.card_id)
		)[0]
		if count == 0:
			db.execute("""
				INSERT INTO SessionCard (session_id, card_id)
				VALUES (?, ?)
				""",
				substitutions=(self.session_id, 
					self.card_id)
			)

	@staticmethod
	def first_review_from_last_day_reviewed_not_in_session(session):
		statement = """
		SELECT AH.card_id, AH.time_to_correct, AH.first_attempt_correct, MIN(AH.answered_at)
		FROM AnswerHistory AH
		JOIN Card C ON C.card_id = AH.card_id
		WHERE AH.session_id <> ? AND C.deck_id = ?
		GROUP BY AH.answered_at_day, AH.card_id
		"""
		db.execute(statement, (session.session_id, session.deck_id))
		rows = db.cursor.fetchall()
		return rows

