from model.db import db

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
			INSERT INTO AnswerHistory (session_id, card_id, time_to_correct, first_attempt_correct, answered_at)
			VALUES (?, ?, ?, ?, ?)
		 	""", (self.session_id, 
		 	   self.card_id, 
		 	   self.time_to_correct, 
		 	   self.first_attempt_correct,
		 	   self.answered_at)
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

