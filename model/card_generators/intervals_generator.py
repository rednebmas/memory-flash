import os
import random
import json
from model.objects.note import Note
from model.objects.interval import Interval
from jinja2 import Environment, FileSystemLoader
import mingus.core.intervals as mingus_intervals

templates = Environment(loader=FileSystemLoader(os.getcwd() + '/view/html'))

class IntervalsGenerator:
	@staticmethod
	def generate_cards():
		notes = [Note(name=name) for name in Note.names()]
		notes = [ 
			"C",
			"D",
			"E",
			"F",
			"G",
			"A",
			"B",

			"C#",
			"D#",
			# "E#",
			"F#",
			"G#",
			"A#",
			# "B#",

			# "Cb",
			"Db",
			"Eb",
			"Gb",
			"Ab",
			"Bb",
		]
		fifths = []
		major_thirds = []
		minor_thirds = []
		fourths = []
		others = []
		uncommon = []
		intervals = Interval.all()
		for note in notes:
			for interval in intervals: # for each interval
				if   abs(interval.half_steps) == 0: continue
				elif note == "E#" or note == "Cb" or note == "B#": arr_to_add_to = uncommon
				elif abs(interval.half_steps) == 7: arr_to_add_to = fifths
				elif abs(interval.half_steps) == 4: arr_to_add_to = major_thirds
				elif abs(interval.half_steps) == 3: arr_to_add_to = minor_thirds
				elif abs(interval.half_steps) == 5: arr_to_add_to = fourths
				else: arr_to_add_to = others

				answer = mingus_intervals.from_shorthand(note, interval.mingusname(), interval.half_steps > 0)
				arr_to_add_to.append(IntervalsGenerator.card_with(Note(note), answer, interval))

		random.shuffle(others)
		random.shuffle(uncommon)
		cards = fifths + major_thirds + minor_thirds + fourths + others + uncommon
		return cards

	@staticmethod
	def card_with(question_note, answer, interval):
		n = 'n' if interval.shortdir()[0] == 'a' else ''
		interval_name = interval.name().lower()
		interval_name = r'<strong>'+interval_name[0]+r'</strong>'+interval_name[1:]

		shortname = interval.shortname()
		direction = "↑" if interval.half_steps > 0 else "↓"

		return {
			"template_path" : 'cards/interval.html',
			"template_data" : json.dumps({
				'interval' : shortname, 
				'direction' : direction, 
				'note' : question_note.pretty_name
			}),
			"answer" : answer,
			"answer_validator" : 'multipleOptions_equals_midiEnharmonicsValid',
			"scale" : question_note.name + " " + ("major" if interval.quality_long == "perfect" else interval.quality_long)
		}
