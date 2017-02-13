import os
import random
import copy
import json
from model.objects.note import Note
from model.objects.chord import Chord
from model.objects.interval import Interval
from jinja2 import Environment, FileSystemLoader
import mingus.core.progressions as progressions

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
	def two_7_five_7_one_M7__root_three_seven__cards():
		chords = []
		notes = [Note(name) for name in Note.names_with_enharmonics()]
		progression = ["ii7", "V7", "IM7"]
		for root_note in notes:
			if root_note.name in ['D#', 'A#', 'G#']: # theoretical keys
				continue

			mingus_chords = copy.deepcopy(progressions.to_chords(progression, root_note.name))
			for chord in mingus_chords:
				del chord[2]

			one_chord = Chord(mingus_chords[2][0])
			two_chord = Chord(mingus_chords[0][0])
			five_chord = Chord(mingus_chords[1][0])

			two_chord.notes = [Note(name) for name in mingus_chords[0]]
			five_chord.notes = [Note(name) for name in mingus_chords[1]]
			five_chord.notes[1], five_chord.notes[2] = five_chord.notes[2], five_chord.notes[1] # switch 3 and 7
			one_chord.notes = [Note(name) for name in mingus_chords[2]]

			chord_prog = [two_chord, five_chord, one_chord]

			chords.append(ProgressionGenerator.card_from_two_five_one(chord_prog, [
				"-inv-ov-7.html",
				"-inv-un-7.html",
				"-inv-ov-maj7.html"
			]))

			# other inversion
			one_chord.notes[1], one_chord.notes[2] = one_chord.notes[2], one_chord.notes[1] 
			five_chord.notes[1], five_chord.notes[2] = five_chord.notes[2], five_chord.notes[1]
			two_chord.notes[1], two_chord.notes[2] = two_chord.notes[2], two_chord.notes[1] 

			chords.append(ProgressionGenerator.card_from_two_five_one(chord_prog, [
				"-inv-un-7.html",
				"-inv-ov-7.html",
				"-inv-un-maj7.html"
			]))

		return chords

	@staticmethod
	def card_from_two_five_one(chords, template_suffixes):
		template_root = 'cards/chord-progression/chord-progression'
		return {
			"template_path" : template_root + '.html',
			"template_data" : json.dumps({
				'chords' : [
					{ 
						"symbol" : "ii", 
						"template_path" : template_root + template_suffixes[0] # "-inv-ov-7.html"
					}, 
					{ 
						"symbol" : "V",
						"template_path" : template_root + template_suffixes[1] #"-inv-un-7.html"
					}, 
					{
						"symbol" : "I", 
						"template_path" : template_root + template_suffixes[2] # "-inv-ov-maj7.html"
					}
				], 
				'root' : chords[-1].root.name
			}),
			"answer" : '→'.join( [' '.join([note.name for note in chord.notes]) for chord in chords] ),
			"answer_validator" : 'equals',
			"accidental" : chords[-1].scale.accidental.symbol,
			"scale" : chords[-1].root.name
		}

	@staticmethod
	def card_from_four_five_one(chords):
		template_root = 'cards/chord-progression/chord-progression'
		return {
			"template_path" : template_root + '.html',
			"template_data" : json.dumps({
				'chords' : [
					{
						"symbol" : "IV", 
						"template_path" : template_root + "-inv-" + str(chords[0].inversion) + ".html"
					}, 
					{
						"symbol" : "V",
						"template_path" : template_root + "-inv-" + str(chords[1].inversion) + ".html"
					}, 
					{
						"symbol" : "I",
						"template_path" : template_root + "-inv-" + str(chords[2].inversion) + ".html" 
					}
				], 
				'root' : chords[-1].root.name
			}),
			"answer" : '→'.join( [' '.join([note.name for note in chord.notes]) for chord in chords] ),
			"answer_validator" : 'equals',
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



