import unittest
from model.validators import exists
from model.db import db
from model.exceptions import ValidationError

class TestValidators(unittest.TestCase):
	pass
	# def setUp(self):
	# 	db.unittest_reset()
	# 	db.execute("""CREATE TABLE ATestClass (
	# 		id INTEGER PRIMARY KEY AUTOINCREMENT,
	# 		descr VARCHAR(64) 
	# 	)""")
	# 	db.execute("INSERT INTO ATestClass (descr) VALUES ('a value')")

	# def test_exists_success(self):
	# 	this = self
	# 	class a_test_class:
	# 		def perform_assertion(self):
	# 			error = exists({'descr': 'a value'})
	# 			this.assertEqual(error, True)

	# 	test_class = a_test_class()
	# 	test_class.perform_assertion()

	# def test_exists_fail(self):
	# 	this = self
	# 	class a_test_class:
	# 		def perform_assertion(self):
	# 			error = exists({'descr': 'the wrong value'})
	# 			this.assertEqual(error, ['descr'])

	# 	test_class = a_test_class()
	# 	test_class.perform_assertion()

def main():
	unittest.main()

if __name__ == '__main__':
	main()