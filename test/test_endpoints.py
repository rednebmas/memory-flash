from main import app
from model.db import db
from model.migration_manager import MigrationManager
from ujson import loads as json_loads
import main
import aiohttp
import unittest

class ALiveSession:
	"""
	Instead of app.test_client.get, use 

		with ALiveSession as session:
			session.test_client.get

	and, add the following parameter to the request

		cookies={ 'session': session.session_id }
	"""
	def __enter__(self):
		global app
		self.test_client = app.test_client
		self.session_id = 'c52b7116c7c44f89a6a0ca3245c30ece'

		# user needs to be logged in to test this endpoint
		@app.listener('after_server_start')
		async def notify_server_started(app, loop):
			# login 
			response = await self.test_client._local_request(
				'POST',
				'/user/login', 
				data="login=FAKE_test_USER&password=pass", 
				headers={ 'Content-Type': "application/x-www-form-urlencoded" }, 
				cookies={ 'session': self.session_id }
			)
		return self

	def __exit__(self, type, value, traceback):
		global app
		# remove listener
		app.listeners['after_server_start'].pop()

class TestEndpoints(unittest.TestCase):
	def test_root(self):
		global app
		request, response = app.test_client.get('/')
		self.assertTrue(response.status == 200)

	def test_decks_endpoint(self):
		global app
		request, response = app.test_client.get('/decks')
		self.assertTrue(response.status == 200, response.body)

	def test_decks_cards(self):
		global app
		request, response = app.test_client.get('/decks/1/cards')
		self.assertTrue(response.status == 200, response.body)

	def test_decks_study(self):
		global app
		request, response = app.test_client.get('/decks/1/study')
		self.assertTrue(response.status == 200, response.body)

	def test_session_next_card(self):
		global app

		with ALiveSession() as session:
			request, response = session.test_client.get(
				'/session/1/next_card?deck_id=1',
				cookies={ 'session': session.session_id }
			)
			self.assertTrue(response.status == 200, response.body)
			self.assertTrue('card_id' in json_loads(response.body))

	def test_card_answer(self):
		global app
		import json

		db.unittest_reset()

		with ALiveSession() as session:
			request, response = session.test_client.post('/card/1/answer', 
				data=json.dumps({"session_id":1,
						"card_id":1,
						"user_id":1,
						"time_to_correct":3.1,
						"first_attempt_correct":True}),
				cookies={ 'session': session.session_id }
			)
			self.assertTrue(response.status == 200, response.body)
			self.assertTrue(json_loads(response.body)['success'])

	def test_create_account(self):
		global app
		request, response = app.test_client.get('/user/create_account')
		self.assertTrue(response.status == 200, response.body)

	def test_create_user(self):
		db.unittest_reset()
		num_users = len(db.select(table="User"))
		request, response = app.test_client.post(
			'/user', 
			data="user_name=sam&email=test%40me.com&password=test", 
			headers={ 'Content-Type': "application/x-www-form-urlencoded" }
		)
		self.assertTrue(response.status == 200, response.body)
		self.assertEqual(len(db.select(table="User")), num_users + 1)

	def test_login_endpoint(self):
		global app
		request, response = app.test_client.get('/user/login')
		self.assertTrue(response.status == 200, response.body)

	def test_user_authenticated(self):
		db.unittest_reset()
		num_users = len(db.select(table="User"))
		request, response = app.test_client.post(
			'/user', 
			data="user_name=sam&email=test%40me.com&password=test", 
			headers={ 'Content-Type': "application/x-www-form-urlencoded" },
		)
		self.assertEqual(len(db.select(table="User")), num_users + 1)
		self.assertTrue(response.status == 200, response.status)

		# username
		request, response = app.test_client.post(
			'/user/login', 
			data="login=sam&password=test", 
			headers={ 'Content-Type': "application/x-www-form-urlencoded" }
		)
		self.assertTrue(response.status == 200, response.status)

		# email
		request, response = app.test_client.post(
			'/user/login', 
			data="login=test%40me.com&password=test", 
			headers={ 'Content-Type': "application/x-www-form-urlencoded" }
		)
		self.assertTrue(response.status == 200, response.status)

	def test_user_not_authenticated(self):
		db.unittest_reset()
		request, response = app.test_client.post(
			'/user', 
			data="user_name=sam&email=test%40me.com&password=test", 
			headers={ 'Content-Type': "application/x-www-form-urlencoded" }
		)
		request, response = app.test_client.post(
			'/user/login', 
			data="login=sam&password=wrong_password", 
			headers={ 'Content-Type': "application/x-www-form-urlencoded" }
		)
		self.assertTrue(response.status == 401, response.status)

def main():
	unittest.main()

if __name__ == '__main__':
	main()