import unittest
from model.migration_manager import MigrationManager
from model.db import DB

class TestMigrationManager(unittest.TestCase):

	def test_created_db(self):
		table_names = ['Deck', 'Card', 'Session', 'AnswerHistory', 'SessionCard']
		db = DB(':memory:')
		MigrationManager.create_db(db)
		tables = db.select(table="sqlite_master", where="type = 'table'", columns="name")
		tables_in_db = [table['name'] for table in tables]
		for table in table_names:
			self.assertTrue(table in tables_in_db)

	def test_insert_all_pregenerated_decks_and_create_db(self):
		db = DB(':memory:')
		try:
			MigrationManager.insert_all_pregenerated_decks_and_create_db(db)
		except Exception as e:
			self.assertTrue(False, e)

def main():
	unittest.main()

if __name__ == '__main__':
	main()