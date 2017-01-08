import unittest
from model.db import DB
from model.migration_manager import MigrationManager

class TestDB(unittest.TestCase):
	def test_insert_key_value_pairs(self):
		db = DB(':memory:')
		MigrationManager.create_db(db)
		# tables = db.select(table="sqlite_master", where="type = 'table'", columns="name")
		# tables_in_db = [table['name'] for table in tables]
		# print('lalalala')
		# print(tables_in_db)

		db.insert_key_value_pairs("Deck", [{'name':'DeckName'}, {'name':'DeckName2'}])
		rows = db.select(table="Deck")
		self.assertTrue(len(rows) == 2)

	def test_execute_statments(self):
		db = DB(':memory:')
		MigrationManager.create_db(db)
		stmts = ['INSERT INTO Deck (name) VALUES ("DeckName")', 'INSERT INTO Deck (name) VALUES ("DeckName2")']
		db.execute_statments(stmts)

		rows = db.select(table="Deck")
		self.assertTrue(len(rows) == 2)

	def test_put_substitutions_in_statement_with_int(self):
		result = DB.put_substitutions_in_statement("1 + ? = 2", (1,))
		self.assertTrue(result == "1 + 1 = 2", result)

def main():
	unittest.main()

if __name__ == '__main__':
	main()