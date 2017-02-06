import os
from model.objects.note import Note
from model.objects.interval import Interval
from jinja2 import Environment, FileSystemLoader

templates = Environment(loader=FileSystemLoader(os.getcwd() + '/view/html'))

class NotesGenerator:
	@staticmethod
	def treble_cards():
		cards = []
		notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
		current_note = Note(name='G3')
		end_note = Note(name='G#6')
		while current_note.freq < end_note.freq:
			cards.append(NotesGenerator.card_for_note(current_note, "treble"))
			current_note = current_note.transposed(Interval(1))
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
