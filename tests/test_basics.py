import os
import sys
import inspect

import unittest

# Import from parent folder
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from website import create_app
  
class BasicTests(unittest.TestCase):

    # Executed before to each test
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
    
    # Executed after each test
    def tearDown(self):
        pass
    
    def test_main_page(self):
        """
        Check if home page responds with status code 200.
        """
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_map_page(self):
        """
        Check if map page responds with status code 200.
        """
        response = self.app.get('/helsinki', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_support_page(self):
        """
        Check if support page responds with status code 200.
        """
        response = self.app.get('/support', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
if __name__ == "__main__":
    unittest.main()