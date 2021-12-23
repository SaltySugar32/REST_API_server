""" Test for CI/CD pipeline """
import unittest
from main import app as rest_api


class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = rest_api.test_client()

    def test_home(self):
        response = self.app.get("/")
        self.assertEqual(response.json, "SaltySugar REST_API_server")


if __name__ == "__main__":
    with rest_api.app_context():
        unittest.main()
