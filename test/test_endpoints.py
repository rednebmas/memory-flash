from sanic.utils import sanic_endpoint_test
from main import app
import aiohttp
import unittest

class TestEndpoints(unittest.TestCase):

	def test_root(self):
		global app
		request, response = sanic_endpoint_test(app, uri='/')
		self.assertTrue(response.status == 200)

def main():
	unittest.main()

if __name__ == '__main__':
	main()