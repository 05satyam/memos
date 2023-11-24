import unittest
from main import app

class BasicTests(unittest.TestCase):

    # Setup and teardown
    def setUp(self):
        self.app = app.test_client()


    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_job(self):
        response = self.app.post('/', data=dict(job="Test Job"))
        self.assertEqual(response.status_code, 302)  # Redirects after adding

if __name__ == '__main__':
    unittest.main()