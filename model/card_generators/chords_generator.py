import os
import random
from jinja2 import Environment, FileSystemLoader
from model.objects.note import Note
from model.objects.chord import Chord

templates = Environment(loader=FileSystemLoader(os.getcwd() + '/view/html'))

class ChordsGenerator:
	@staticmethod
	def generate_triad(suffix=''):
		roots = []
		inversions = []
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
		uncommon = []
		for note in notes:
			chord_root = Chord(note + suffix)
			chord_first_inversion = chord_root.invert(1)
			chord_second_inversion = chord_root.invert(2)

			# i don't really care about double sharps at the moment...
			root_accidentals = [n.name[1:] for n in chord_root.notes]
			if '##' in root_accidentals or 'bb' in root_accidentals:
				continue

			if note == "E#" or note == "Cb" or note == "B#":
				uncommon.append(chord_root)
				uncommon.append(chord_first_inversion)
				uncommon.append(chord_second_inversion)
			else:
				roots.append(chord_root)
				inversions.append(chord_first_inversion)
				inversions.append(chord_second_inversion)

		random.shuffle(roots)
		random.shuffle(inversions)
		random.shuffle(uncommon)
		cards = list(map(ChordsGenerator.card_for_chord, roots + inversions + uncommon))
		return cards

	@staticmethod
	def generate_major_chord_cards():
		return ChordsGenerator.generate_triad()

	@staticmethod
	def generate_minor_chord_cards():
		return ChordsGenerator.generate_triad('m')

	@staticmethod
	def generate_major_and_minor_chord_cards():
		cards = ChordsGenerator.generate_major_chord_cards() + ChordsGenerator.generate_minor_chord_cards()
		random.shuffle(cards)
		return cards

	@staticmethod
	def generate_dim_chords_cards():
		return ChordsGenerator.generate_triad('dim')

	@staticmethod
	def generate_aug_chords_cards():
		return ChordsGenerator.generate_triad('aug')
 
	@staticmethod
	def card_for_chord(chord):
		return {
			"question" : templates.get_template('cards/chord.html').render(chord=chord),
			"answer" : ' '.join([note.name for note in chord.notes]),
			"answer_validator" : 'multipleOptions_equals_midiEnharmonicsValid',
			"scale" : chord.root.name + " " + chord.quality_full()
		}

