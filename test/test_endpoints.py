from sanic.utils import sanic_endpoint_test
from main import app
from model.db import DB
from model.migration_manager import MigrationManager
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

def main():
	unittest.main()

if __name__ == '__main__':
	main()