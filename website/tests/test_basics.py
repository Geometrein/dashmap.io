"""
Main Unit Tests.
"""
import os
import sys
import inspect

import unittest

from website import create_app

# Import from parent folder
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


class BasicTests(unittest.TestCase):
    """
    Basic test case class.
    """
    # Executed before to each test
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_main_page_get_response(self):
        """
        Check if home page responds with status code 200.
        """
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_map_page_get_response(self):
        """
        Check if map page responds with status code 200.
        """
        response = self.app.get('/helsinki', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_404_response(self):
        """
        Check if random endpoint responds with status code 404.
        """
        response = self.app.get('/a_random_walk_on_a_quantum_string', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_response(self):
        """
        Check if random endpoint responds with status code 404.
        """
        response = self.app.get('/a_random_walk_on_a_quantum_string', follow_redirects=True)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
