import unittest
from unittest import mock

import main
from main import app
import fakeredis

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.redis_patcher = mock.patch('main.redis_client', fakeredis.FakeStrictRedis())
        self.redis_patcher.start()
        app.redis_client = main.redis.Redis(decode_responses=True)
        main.app.testing = True
        self.app = main.app.test_client()

    def tearDown(self):
        self.redis_patcher.stop()

    def test_add_job(self):
        response = self.app.post('/add', data={'title': 'Test Job', 'company': 'Test Company', 'status': 'Open'})
        self.assertEqual(response.status_code, 302)

    def test_get_jobs(self):
        self.app.post('/add', data={'title': 'Test Job', 'company': 'Test Company', 'status': 'Open'})
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
