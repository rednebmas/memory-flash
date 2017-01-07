class TimesTableGenerator:
	@staticmethod
	def generate_cards(n=12):
		"""Generate the times tables as cards
		Return:
			an array dictionaries which represent card objects
		"""
		cards = []
		for i in range(1, n +1):
			for j in range(1, n + 1):
				cards.append({
						"question" : "What is {} * {}".format(i, j),
						"answer" : str(i*j)
				})
		return cards