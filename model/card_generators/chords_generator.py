import os
from jinja2 import Environment, FileSystemLoader
from model.objects.note import Note
from model.objects.chord import Chord

templates = Environment(loader=FileSystemLoader(os.getcwd() + '/view/html'))

class ChordsGenerator:
	@staticmethod
	def generate_major_chord_cards():
		cards = []
		notes = [Note(name=name) for name in Note.names_with_enharmonics()]
		for note in notes:
			chord_root = Chord(note.name)
			chord_first_inversion = Chord(note.name).inversion(1)
			chord_second_version = Chord(note.name).inversion(2)

			cards += map(ChordsGenerator.card_for_chord, [chord_root, chord_first_inversion, chord_second_version])
		return cards

	@staticmethod
	def card_for_chord(chord):
		return {
			"question" : templates.get_template('cards/chord.html').render(chord=chord),
			"answer" : ' '.join([note.name for note in chord.notes])
		}

