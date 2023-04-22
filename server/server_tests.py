import unittest
from server import app

class TestServer(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_singleCourse(self):
        response = self.app.get('/coursedetails?coursename="History%20and%20Policy%20for%20CLD"&term="Fall"&year=2020')
        print('Response:',response)
        self.assertEqual(response.status_code, 200)
