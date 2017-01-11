import unittest
from model.objects.accidental import Accidental

class TestAccidental(unittest.TestCase):
	def test_equal(self):
		flat = Accidental.flat
		self.assertTrue(flat == Accidental.flat)

	def test_to_str(self):
		flat = Accidental.flat
		self.assertTrue(str(flat) == 'flat', str(flat))

def main():
	unittest.main()

if __name__ == '__main__':
	main()