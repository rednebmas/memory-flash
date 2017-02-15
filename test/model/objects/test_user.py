import unittest
from model.objects.user import User
from model.db import db
from model.objects.exceptions import ValidationError

class TestUser(unittest.TestCase):
    def setUp(self):
        db.unittest_reset()

    def test_user_created(self):
        num_users = len(db.select(table="User"))
        User.create('sam.i.am', 'fake@email.com', 'password')
        self.assertEqual(len(db.select(table="User")), num_users + 1)

    def test_user_not_created_if_duplicate_user_name(self):
        def createUser():
            User.create('sam.i.am', 'fake@email.com', 'password')
        createUser()
        self.assertRaises(ValidationError, createUser)

    def test_user_not_created_if_duplicate_user_email(self):
        User.create('sam.i.am1', 'fake@email.com', 'password')
        def createUser():
            User.create('sam.i.am2', 'fake@email.com', 'password')
        self.assertRaises(ValidationError, createUser)

    def test_password_hashed(self):
        the_password = 'password'
        User.create('sam.i.am1', 'fake@email.com', the_password)
        stored_password = db.select1(table="User", where="email = 'fake@email.com'")['password']
        self.assertNotEqual(stored_password, the_password)

def main():
	unittest.main()

if __name__ == '__main__':
	main()