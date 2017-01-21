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
			"answer" : note.name_octave
		}

	@staticmethod
	def generate_cards():
		return NotesGenerator.treble_cards()
		"""Generate the notes cards using images
		Return:
			an array dictionaries which represent card objects
		"""
		cards = []
		notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
		for note in notes:
			for i in range(0, 4):
				cards.append({
						"question" : """
						<style>
						  img.note {
						  	width: 100%%;
						  }
						  div.question {
						  	text-align: center;
						  }
						  div.note-img-container {
						  	width: 118px;
						  	height: 148px;
						  	text-align: center;
						  	margin: auto;
						  }
						</style	>
						<p>What note is this?</p>
						<div class="note-img-container"><img class="note" src="/img/treble_%(file_name)s.png"></div>
						""" % { 'file_name': note + str(i) },
						"answer" : note
				})
				cards.append({
						"question" : """
						<style>
						  img.note {
						  	width: 100%%;
						  }
						  div.question {
						  	text-align: center;
						  }
						  div.note-img-container {
						  	width: 118px;
						  	height: 148px;
						  	text-align: center;
						  	margin: auto;
						  }
						</style	>
						<p>What note is this?</p>
						<div class="note-img-container"><img class="note" src="/img/bass_%(file_name)s.png"></div>
						""" % { 'file_name': note + str(i) },
						"answer" : note
				})

		return cards