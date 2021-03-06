class Accidental:
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return self.name

	def __eq__(self, other):
		"""Override the default Equals behavior"""
		if isinstance(other, self.__class__):
			return other.name == self.name
		return False

	def __ne__(self, other):
		"""Define a non-equality test"""
		return not self.__eq__(other)

	@property
	def symbol(self):
		if self.name == 'doubleflat':
			return 'bb'
		if self.name == 'flat':
			return 'b'
		elif self.name == 'sharp':
			return '#'
		else:
			return ''

	@property
	def pretty_symbol(self):
		if self.name == 'doubleflat':
			return '♭♭'
		if self.name == 'flat':
			return '♭'
		elif self.name == 'sharp':
			return '#'
		else:
			return ''

class Accidental:
	doubleflat = Accidental('doubleflat')
	flat = Accidental('flat')
	sharp = Accidental('sharp')
	natural = Accidental('natural')
