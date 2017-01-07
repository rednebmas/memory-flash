import unittest
from model.migration_manager import MigrationManager
from model.db import DB

class TestMigrationManager(unittest.TestCase):

	def test_tables_created(self):
		table_names = ['Deck', 'Card', 'Session', 'AnswerHistory', 'SessionCard']
		db = DB(':memory:')
		MigrationManager.create_db(db)
		tables = db.select(table="sqlite_master", where="type = 'table'", columns="name")
		tables_in_db = [table['name'] for table in tables]
		for table in table_names:
			self.assertTrue(table in tables_in_db)

def main():
	unittest.main()

if __name__ == '__main__':
	main()