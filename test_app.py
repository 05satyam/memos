import unittest
from main import app

class BasicTests(unittest.TestCase):
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_job(self):
        response = self.app.post('/add', data=dict(title="Test Job", company="Test Company", status="Applied"))
        self.assertEqual(response.status_code, 302)  # Redirects after adding

if __name__ == '__main__':
    unittest.main()