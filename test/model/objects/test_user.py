import unittest
from model.objects.user import User
from model.db import db
from model.exceptions import ValidationError

the_password = 'password'
not_the_password = 'not the password'

class TestUser(unittest.TestCase):

    def setUp(self):
        db.unittest_reset()

    def test_user_created(self):
        num_users = len(db.select(table="User"))
        user = User.create('sam.i.am', 'fake@email.com', 'password')
        self.assertEqual(len(db.select(table="User")), num_users + 1)
        self.assertEqual(user.user_name, 'sam.i.am')

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
        User.create('sam.i.am1', 'fake@email.com', the_password)
        stored_password = db.select1(table="User", where="email = 'fake@email.com'")['password']
        self.assertNotEqual(stored_password, the_password)

    def test_authenticate_success(self):
        User.create('sam.i.am1', 'fake@email.com', the_password)
        user = User.authenticate('sam.i.am1', the_password)
        self.assertTrue(user.user_id > 0)
        user = User.authenticate('fake@email.com', the_password)
        self.assertTrue(user.user_id > 0)

    def test_authenticate_failure(self):
        User.create('sam.i.am1', 'fake@email.com', the_password)
        def auth():
            user = User.authenticate('sam.i.am1', not_the_password)
        self.assertRaises(ValidationError, auth)

def main():
	unittest.main()

if __name__ == '__main__':
	main()