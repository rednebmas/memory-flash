import os
# from model.objects.note import Note
from model.objects.interval import Interval
from jinja2 import Environment, FileSystemLoader
from mingus.containers import Note

templates = Environment(loader=FileSystemLoader(os.getcwd() + '/view/html'))

class NotesGenerator:
	@staticmethod
	def treble_cards():
		cards = []
		current_note = Note('G-3')
		end_note = Note('G#-6')
		while int(current_note) < int(end_note):
			cards.append(NotesGenerator.card_for_note(current_note, "treble"))
			current_note = current_note.from_int(int(current_note) + 1)
		return cards

	@staticmethod
	def card_for_note(note, staff):
		return {
			"question" : templates.get_template('cards/note-staff.html').render(note=note, staff=staff),
			"answer" : note.name,
			"answer_validator" : 'answerValidator_equals_midiEnharmonicsValid'
		}

	@staticmethod
	def generate_cards():
		return NotesGenerator.treble_cards()
