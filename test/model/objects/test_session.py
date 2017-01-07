import unittest
from model.objects.session import Session

class TestSession(unittest.TestCase):
	def test_from_deck_id(self):
		sesh = Session.from_deck_id(1)
		self.assertTrue(sesh is not None)
		self.assertTrue(isinstance(sesh.session_id, int))

def main():
	unittest.main()

if __name__ == '__main__':
	main()