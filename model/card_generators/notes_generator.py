import os
# from model.objects.note import Note
import json
from model.objects.interval import Interval
from jinja2 import Environment, FileSystemLoader
from mingus.containers import Note

templates = Environment(loader=FileSystemLoader(os.getcwd() + '/view/html'))

class NotesGenerator:
	@staticmethod
	def treble_cards():
		cards = []
		current_note = Note('F-3')
		end_note = Note('G#-6')
		while int(current_note) < int(end_note):
			if '#' in current_note.name or 'b' in current_note.name:
				current_note = current_note.from_int(int(current_note) + 1)
				continue

			cards.append(NotesGenerator.card_for_note(current_note, "treble"))
			current_note = current_note.from_int(int(current_note) + 1)
		return cards

	@staticmethod
	def bass_cards():
		cards = []
		current_note = Note('F-3')
		end_note = Note('F-1')
		while int(current_note) < int(end_note):
			if '#' in current_note.name or 'b' in current_note.name:
				current_note = current_note.from_int(int(current_note) + 1)
				continue

			cards.append(NotesGenerator.card_for_note(current_note, "bass"))
			current_note = current_note.from_int(int(current_note) + 1)
		return cards

	@staticmethod
	def card_for_note(note, clef):
		return {
			"template_path" : "cards/note-staff.html",
			"template_data" : json.dumps({
				'note': note.name, 
				'octave': note.octave, 
				'clef': clef
			}),
			"answer" : note.name + str(note.octave),
			"answer_validator" : 'equals_octave'
		}

	@staticmethod
	def generate_cards():
		return NotesGenerator.treble_cards() + NotesGenerator.bass_cards()
