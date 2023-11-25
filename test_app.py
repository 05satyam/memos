import unittest
from unittest import mock

from main import app
import fakeredis

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        self.app = app.test_client()
        self.redis_patcher = mock.patch('app.redis_client', fakeredis.FakeStrictRedis())
        self.redis_patcher.start()

    def tearDown(self):
        self.redis_patcher.stop()

    def test_add_job(self):
        response = self.app.post('/add', data={'title': 'Test Job', 'company': 'Test Company', 'status': 'Open'})
        self.assertEqual(response.status_code, 201)

    def test_get_jobs(self):
        self.app.post('/add', data={'title': 'Test Job', 'company': 'Test Company', 'status': 'Open'})
        response = self.app.get('/jobs')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Job', response.data.decode())

if __name__ == '__main__':
    unittest.main()
