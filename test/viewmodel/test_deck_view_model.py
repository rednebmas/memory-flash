import unittest
from model.db import db
import viewmodel.deck_view_model as deck_view_model
from viewmodel.deck_view_model import DeckViewModel
from model.migration_manager import MigrationManager

class TestDeckViewModel(unittest.TestCase):

	def test_all_decks(self):
		db.unittest_reset()
		self.assertTrue(len(DeckViewModel.all_decks()) > 0)


def main():
	unittest.main()

if __name__ == '__main__':
	main()