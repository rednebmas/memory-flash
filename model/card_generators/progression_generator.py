import os
import random
from model.objects.note import Note
from model.objects.chord import Chord
from model.objects.interval import Interval
from jinja2 import Environment, FileSystemLoader

templates = Environment(loader=FileSystemLoader(os.getcwd() + '/view/html'))

class ProgressionGenerator:
	@staticmethod
	def four_five_one_cards():
		root_inversion = []
		first_inversion = []
		second_inversion = []
		notes = [Note(name) for name in Note.names_with_enharmonics()]
		for root_note in notes:
			if root_note.name in ['D#', 'A#', 'G#']: # theoretical keys
				continue
			root_inversion_chords = ProgressionGenerator.four_five_one_from_one(root_note, 2, 1, 0)
			first_inversion_chords = ProgressionGenerator.four_five_one_from_one(root_note, 0, 2, 1)
			second_inversion_chords = ProgressionGenerator.four_five_one_from_one(root_note, 1, 0, 2)

			root_inversion.append(ProgressionGenerator.card_from_four_five_one(root_inversion_chords))
			first_inversion.append(ProgressionGenerator.card_from_four_five_one(first_inversion_chords))
			second_inversion.append(ProgressionGenerator.card_from_four_five_one(second_inversion_chords))

		random.shuffle(root_inversion)
		random.shuffle(first_inversion)
		random.shuffle(second_inversion)
		return root_inversion + first_inversion + second_inversion

	@staticmethod
	def card_from_four_five_one(chords):
		return {
			"question" : templates.get_template('cards/chord-progression/chord-progression.html').render(
				symbols=["IV", "V", "I"], 
				chords=chords, 
				root=chords[-1].root
				),
			"answer" : '→'.join( [' '.join([note.name for note in chord.notes]) for chord in chords] ),
			"answer_validator" : 'multipleOptions_equals_midiEnharmonicsValid',
			"accidental" : chords[-1].scale.accidental.symbol,
			"scale" : chords[-1].root.name
		}

	@staticmethod
	def four_five_one_from_one(one, four_inversion, five_inversion, one_inversion):
		one_chord = Chord(one.name).invert(one_inversion)

		four = one_chord.scale.degree(4)
		five = one_chord.scale.degree(5)

		four_chord = Chord(four.name).invert(four_inversion)
		five_chord = Chord(five.name).invert(five_inversion)

		return [four_chord, five_chord, one_chord]



