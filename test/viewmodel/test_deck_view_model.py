import unittest
from model.db import DB
import viewmodel.deck_view_model as deck_view_model
from viewmodel.deck_view_model import DeckViewModel
from model.migration_manager import MigrationManager

class TestDeckViewModel(unittest.TestCase):

	def test_all_decks(self):
		db = DB(':memory:')
		MigrationManager.insert_all_pregenerated_decks_and_create_db(db)
		deck_view_model.db = db
		self.assertTrue(len(DeckViewModel.all_decks()) > 0)


def main():
	unittest.main()

if __name__ == '__main__':
	main()