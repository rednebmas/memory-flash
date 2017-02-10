import os
import random
from jinja2 import Environment, FileSystemLoader
from model.objects.note import Note
from model.objects.chord import Chord

templates = Environment(loader=FileSystemLoader(os.getcwd() + '/view/html'))

class ChordsGenerator:
	@staticmethod
	def generate_major_chord_cards():
		roots = []
		inversions = []
		notes = [Note(name=name) for name in Note.names_with_enharmonics()]
		for note in notes:
			chord_root = Chord(note.name)
			chord_first_inversion = Chord(note.name).invert(1)
			chord_second_inversion = Chord(note.name).invert(2)

			roots.append(chord_root)
			inversions.append(chord_first_inversion)
			inversions.append(chord_second_inversion)

		random.shuffle(roots)
		random.shuffle(inversions)
		cards = list(map(ChordsGenerator.card_for_chord, roots + inversions))
		return cards

	@staticmethod
	def generate_minor_chord_cards():
		roots = []
		inversions = []
		notes = [Note(name=name) for name in Note.names_with_enharmonics()]
		for note in notes:
			chord_root = Chord(note.name + 'm')
			chord_first_inversion = Chord(note.name + 'm').invert(1)
			chord_second_inversion = Chord(note.name + 'm').invert(2)

			roots.append(chord_root)
			inversions.append(chord_first_inversion)
			inversions.append(chord_second_inversion)

		random.shuffle(roots)
		random.shuffle(inversions)
		cards = list(map(ChordsGenerator.card_for_chord, roots + inversions))
		return cards

	@staticmethod
	def generate_major_and_minor_chord_cards():
		cards = ChordsGenerator.generate_major_chord_cards() + ChordsGenerator.generate_minor_chord_cards()
		random.shuffle(cards)
		return cards


	@staticmethod
	def generate_dim_chords_cards():
		roots = []
		inversions = []
		notes = [Note(name=name) for name in Note.names_with_enharmonics()]
		for note in notes:
			chord_root = Chord(note.name + 'dim')
			chord_first_inversion = chord_root.invert(1)
			chord_second_inversion = chord_root.invert(2)

			roots.append(chord_root)
			inversions.append(chord_first_inversion)
			inversions.append(chord_second_inversion)

		random.shuffle(roots)
		random.shuffle(inversions)
		cards = list(map(ChordsGenerator.card_for_chord, roots + inversions))
		return cards

	@staticmethod
	def generate_aug_chords_cards():
		roots = []
		inversions = []
		notes = [Note(name=name) for name in Note.names_with_enharmonics()]
		for note in notes:
			chord_root = Chord(note.name + 'aug')
			chord_first_inversion = chord_root.invert(1)
			chord_second_inversion = chord_root.invert(2)

			# i don't really care about double sharps at the moment...
			# root_accidentals = [n.name[1:] for n in chord_root.notes]
			# if '##' in root_accidentals or 'bb' in root_accidentals:
			# 	continue

			roots.append(chord_root)
			inversions.append(chord_first_inversion)
			inversions.append(chord_second_inversion)

		random.shuffle(roots)
		random.shuffle(inversions)
		cards = list(map(ChordsGenerator.card_for_chord, roots + inversions))
		return cards

 
	@staticmethod
	def card_for_chord(chord):
		return {
			"question" : templates.get_template('cards/chord.html').render(chord=chord),
			"answer" : ' '.join([note.name for note in chord.notes]),
			"answer_validator" : 'multipleOptions_equals_midiEnharmonicsValid'
		}

