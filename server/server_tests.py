import unittest
from unittest import mock
import json
from server import app
import requests

class TestServer(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.testCount = 1

    def test_mockData(self):

        with mock.patch('requests.get') as mock_get:

            # Set up mock object
            mock_get.return_value.json.return_value = {'coursename': 'Analysis of Mock'}
        
            # Fetch data with test URL
            data = requests.get('https://127.0.0.1:5000/mockdata').json()
        
            # Assertions
            assert data == {'coursename': 'Analysis of Mock'}
            mock_get.assert_called_with('https://127.0.0.1:5000/mockdata')

            print('Mock test passed!')


    def test_singleCourse(self):
        response = self.app.get('/coursedetails?name="Advanced Computer Graphics"&term="Spring"&year=2022')
        self.assertEqual(response.status_code, 200)

        responseJson = json.loads(response.data)
        self.assertEqual(len(responseJson), 2)

        print('Test passed!')

    def test_getCourseNames(self):

        response = self.app.get('/getcourses?count=10')
        self.assertEqual(response.status_code, 200)

        responseJson = json.loads(response.data)
        self.assertEqual(len(responseJson), 10)

        print('Test passed!')

    def test_getCourseNames1(self):

        response = self.app.get('/getcourses?count=1000')
        self.assertEqual(response.status_code, 200)

        responseJson = json.loads(response.data)
        self.assertLess(len(responseJson), 1000) # At this point, 1000 courses are not there

        print('Test passed!')

    def test_getCourseHistory(self):

        response = self.app.get('/coursehistory?name="Advanced Computer Graphics"')
        self.assertEqual(response.status_code, 200)

        responseJson = json.loads(response.data)
        self.assertGreater(len(responseJson), 0)

        print('Test passed!')

    def test_getCourseHistory1(self):

        response = self.app.get('/coursehistory?name=" "') # Empty Course name
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data, b'null\n') # Response is null
        print('Test passed!')

    def test_courseId(self):

        response = self.app.get('/courseid?name="Advanced-Computer-Graphics"&id=0')
        self.assertEqual(response.status_code, 200)

        responseJson = json.loads(response.data)
        self.assertIsNotNone(responseJson)

        print('Test passed!')

    def test_courseId1(self):

        response = self.app.get('/courseid?name="None"&id=0')
        self.assertEqual(response.status_code, 200)

        responseJson = json.loads(response.data)
        self.assertIsNone(responseJson)

        print('Test passed!')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()