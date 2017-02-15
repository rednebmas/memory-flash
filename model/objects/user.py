import bcrypt
import sys
from model.db import db
from model.objects.exceptions import ValidationError

# less bcrypt rounds for unit testing becuase it's slow
if 'unittest' in sys.argv[0]:
	bcrypt_rounds = 4
else:
	bcrypt_rounds = 12

class User:
	def __init__(self, arg):
		self.arg = arg

	@staticmethod
	def create(user_name, email, password):
		result = db.select("User", where="user_name = ?", substitutions=(user_name,))
		if len(result) > 0:
			raise ValidationError('Username already exists')
		result = db.select("User", where="email = ?", substitutions=(email,))
		if len(result) > 0:
			raise ValidationError('A user with that email already exists')

		hash_password = bcrypt.hashpw(password.encode('UTF_8'), bcrypt.gensalt(bcrypt_rounds))

		db.execute("INSERT INTO User (user_name, email, password) VALUES (?, ?, ?)", 
			substitutions=(user_name, email, hash_password,))

		