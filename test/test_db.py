import unittest
from model.db import DB

class TestDB(unittest.TestCase):
	def test_select(self):
		db = DB(':memory:')
		self.assertTrue(True)

def main():
	unittest.main()

if __name__ == '__main__':
	main()