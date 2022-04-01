import os
import random
import json
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
			chord_inversions = []

			# dim7 chords do not have inversions b/c they equal other root inversion dim7 chords
			if suffix != 'dim7': 
				chord_inversions.append(chord_root.invert(1, True))
				chord_inversions.append(chord_root.invert(2, True))
				if '7' in suffix:
					chord_inversions.append(chord_root.invert(3, True))

			# i don't really care about double sharps at the moment...
			root_accidentals = [n.name[1:] for n in chord_root.notes]
			if '##' in root_accidentals or 'bb' in root_accidentals:
				continue

			if note == "E#" or note == "Cb" or note == "B#":
				uncommon.append(chord_root)
				uncommon += chord_inversions
			else:
				roots.append(chord_root)
				inversions += chord_inversions

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
	def generate_dom7_chords_cards():
		return ChordsGenerator.generate_triad('7')

	@staticmethod
	def generate_maj7_chords_cards():
		return ChordsGenerator.generate_triad('maj7')

	@staticmethod
	def generate_min7_chords_cards():
		return ChordsGenerator.generate_triad('m7')

	@staticmethod
	def generate_m7b5_chords_cards():
		return ChordsGenerator.generate_triad('m7b5')

	@staticmethod
	def generate_dim7_chords_cards():
		return ChordsGenerator.generate_triad('dim7')

	@staticmethod
	def generate_min_maj7_chords_cards():
		return ChordsGenerator.generate_triad('mM7')
 
	@staticmethod
	def card_for_chord(chord):
		if chord.quality_full() == "diminished" or chord.quality_full() == "augmented":
			scale = chord.root.name
		else:
			scale = chord.root.name + ' minor' if 'm' in chord.quality else chord.root.name + ' major'
		return {
			"template_path" : 'cards/chord.html',
			"template_data" : json.dumps({ 'chord_pretty_name' : chord.pretty_name }),
			"answer" : ' '.join([note.name for note in chord.notes]),
			"answer_validator" : 'equals',
			"scale" : scale,
			"accidental" : chord.scale.accidental.symbol
		}
