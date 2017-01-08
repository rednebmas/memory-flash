from model.objects.note import Note
from model.objects.interval import Interval

class IntervalsGenerator:
	@staticmethod
	def generate_cards():
		cards = []
		notes = [Note(name=name) for name in Note.names()]
		for note in notes:
			for i in range(-11, 12): # for each interval
				if i == 0: continue
				interval = Interval(i)
				if note.isaltered():
					flat_note, sharp_note = note.enharmonics()
					answer = note.transposed(interval.half_steps)
					if answer.isaltered():
						flat_answer, sharp_answer = answer.enharmonics()
						cards.append(IntervalsGenerator.card_with(flat_note, flat_answer.name, interval))
						cards.append(IntervalsGenerator.card_with(sharp_note, sharp_answer.name, interval))
					else:
						cards.append(IntervalsGenerator.card_with(flat_note, answer.name, interval))
						cards.append(IntervalsGenerator.card_with(sharp_note, answer.name, interval))
				else:
					answer = note.transposed(interval.half_steps)
					if answer.isaltered():
						flat_answer, sharp_answer = answer.enharmonics()
						cards.append(IntervalsGenerator.card_with(note, flat_answer.name+'|'+sharp_answer.name, interval))
					else:
						cards.append(IntervalsGenerator.card_with(note, answer.name, interval))
		return cards

	@staticmethod
	def card_with(question_note, answer, interval):
		n = 'n' if interval.shortdir()[0] == 'a' else ''
		interval_name = interval.name().lower()
		interval_name = r'<strong>'+interval_name[0]+r'</strong>'+interval_name[1:]

		return {
			"question" : r"""<style>
							 </style>
							 <p>What is a%(n)s %(interval)s of %(question_note)s?</p>
							 """ % {
								'question_note': question_note.pretty_name,
								'interval' : interval_name,
								'n' : n
							 },
			"answer" : answer
		}
