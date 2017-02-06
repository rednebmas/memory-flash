import os
import random
from model.objects.note import Note
from model.objects.interval import Interval
from jinja2 import Environment, FileSystemLoader

templates = Environment(loader=FileSystemLoader(os.getcwd() + '/view/html'))

class IntervalsGenerator:
	@staticmethod
	def generate_cards():
		notes = [Note(name=name) for name in Note.names()]
		fifths = []
		major_thirds = []
		minor_thirds = []
		fourths = []
		others = []
		for note in notes:
			for i in range(-11, 12): # for each interval
				if i == 0: continue

				if abs(i) == 7: arr_to_add_to = fifths
				elif abs(i) == 4: arr_to_add_to = major_thirds
				elif abs(i) == 3: arr_to_add_to = minor_thirds
				elif abs(i) == 5: arr_to_add_to = fourths
				else: arr_to_add_to = others

				interval = Interval(i)
				if note.isaltered():
					flat_note, sharp_note = note.enharmonics()
					answer = note.transposed(interval)
					if answer.isaltered():
						flat_answer, sharp_answer = answer.enharmonics()
						arr_to_add_to.append(IntervalsGenerator.card_with(flat_note, flat_answer.name, interval))
						arr_to_add_to.append(IntervalsGenerator.card_with(sharp_note, sharp_answer.name, interval))
					else:
						arr_to_add_to.append(IntervalsGenerator.card_with(flat_note, answer.name, interval))
						arr_to_add_to.append(IntervalsGenerator.card_with(sharp_note, answer.name, interval))
				else:
					answer = note.transposed(interval)
					if answer.isaltered():
						flat_answer, sharp_answer = answer.enharmonics()
						arr_to_add_to.append(IntervalsGenerator.card_with(note, flat_answer.name+'|'+sharp_answer.name, interval))
					else:
						arr_to_add_to.append(IntervalsGenerator.card_with(note, answer.name, interval))

		random.shuffle(fifths)
		random.shuffle(major_thirds)
		random.shuffle(minor_thirds)
		random.shuffle(fourths)
		random.shuffle(others)

		cards = fifths + major_thirds + minor_thirds + fourths + others
		return cards

	@staticmethod
	def card_with(question_note, answer, interval):
		n = 'n' if interval.shortdir()[0] == 'a' else ''
		interval_name = interval.name().lower()
		interval_name = r'<strong>'+interval_name[0]+r'</strong>'+interval_name[1:]

		shortname = interval.shortname()
		direction = "↑" if interval.half_steps > 0 else "↓"

		return {
			"question" : templates.get_template('cards/interval.html')
						 .render(interval=shortname, direction=direction, note=question_note),
			"answer" : answer,
			"answer_validator" : 'multipleOptions_equals_midiEnharmonicsValid'
		}
