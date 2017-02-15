from sanic.utils import sanic_endpoint_test
from main import app
from model.db import db
from model.migration_manager import MigrationManager
from ujson import loads as json_loads
import main
import aiohttp
import unittest

class TestEndpoints(unittest.TestCase):
	def test_root(self):
		global app
		request, response = sanic_endpoint_test(app, uri='/')
		self.assertTrue(response.status == 200)

	def test_decks_endpoint(self):
		global app
		request, response = sanic_endpoint_test(app, uri='/decks')
		self.assertTrue(response.status == 200, response.body)

	def test_decks_cards(self):
		global app
		request, response = sanic_endpoint_test(app, uri='/decks/1/cards')
		self.assertTrue(response.status == 200, response.body)

	def test_decks_study(self):
		global app
		request, response = sanic_endpoint_test(app, uri='/decks/1/study')
		self.assertTrue(response.status == 200, response.body)

	def test_session_next_card(self):
		global app
		request, response = sanic_endpoint_test(app, uri='/session/1/next_card?deck_id=1')
		self.assertTrue(response.status == 200, response.body)
		self.assertTrue('card_id' in json_loads(response.body))

	def test_card_answer(self):
		global app
		request, response = sanic_endpoint_test(app, uri='/card/1/answer', method="post",
			data="""{"session_id":1,
					"card_id":1,
					"time_to_correct":3.1,
					"first_attempt_correct":true}""")
		self.assertTrue(response.status == 200, response.body)
		self.assertTrue(json_loads(response.body)['success'])

	def test_create_account(self):
		global app
		request, response = sanic_endpoint_test(app, uri='/user/create_account')
		self.assertTrue(response.status == 200, response.body)

	def test_create_user(self):
		db.unittest_reset()
		num_users = len(db.select(table="User"))
		request, response = sanic_endpoint_test(app, 
			uri='/user', 
			method='post',
			data="user_name=sam&email=test%40me.com&password=test", 
			headers={ 'Content-Type': "application/x-www-form-urlencoded" }
		)
		self.assertTrue(response.status == 200, response.body)
		self.assertEqual(len(db.select(table="User")), num_users + 1)

def main():
	unittest.main()

if __name__ == '__main__':
	main()