import bcrypt
import sys
import model.validators as validators
from model.db import db
from model.exceptions import ValidationError

# less bcrypt rounds for unit testing becuase it's slow
if 'unittest' in sys.argv[0]:
	bcrypt_rounds = 4
else:
	bcrypt_rounds = 12

class User:
	def __init__(self, user_id, user_name, email, password):
		self.user_id = user_id
		self.user_name = user_name
		self.email = email
		self.password = password

	@staticmethod
	def from_db(row):
		return User(row['user_id'], row['user_name'], row['email'], row['password'])

	@staticmethod
	def from_db_id(user_id):
		try:
			row = db.select1(table="User", where="user_id = ?", substitutions=(user_id,))
			return User.from_db(row)
		except Exception as e:
			return None

	@staticmethod
	def from_email(email):
		try:
			row = db.select1(table="User", where="email = ?", substitutions=(email,))
			return User.from_db(row)
		except Exception as e:
			return None

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
		return User.from_email(email)

	@staticmethod
	def authenticate(login, password):
		""" Authenticate with username or password """
		def check_credentials(login_col):
			user = db.select1("User", where=login_col + " = ?", substitutions=(login,))
			correct_pw = user['password']
			if bcrypt.checkpw(password.encode('UTF_8'), correct_pw):
				return User.from_db(user)
			else:
				raise ValidationError('Incorrect password. Please try again.')

		if validators.exists({ "user_name" : login }) != True:
			if validators.exists({ "email" : login }) != True:
				raise ValidationError('Username or email does exist.')
			else:
				return check_credentials("email")
		else:
			return check_credentials("user_name")



		