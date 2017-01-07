class NotesGenerator:
	@staticmethod
	def generate_cards():
		"""Generate the notes cards using images
		Return:
			an array dictionaries which represent card objects
		"""
		cards = []
		notes = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
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