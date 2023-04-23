import unittest
import json
import sys
import os
from server import app

class TestServer(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.testCount = 1

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