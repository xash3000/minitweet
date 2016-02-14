import unittest
from base import BaseTestCase


class TestConfigurations(BaseTestCase):

    def test_environment_is_testing(self):
        self.app.config.from_object("config.TestConfig")
        self.assertTrue(self.app.config["TESTING"])
        self.assertFalse(self.app.config["WTF_CSRF_ENABLED"])

    def test_environment_is_development(self):
        self.app.config.from_object("config.DevConfig")
        self.assertTrue(self.app.config["DEBUG"])

    def test_environment_is_production(self):
        self.app.config.from_object("config.ProductionConfig")
        self.assertFalse(self.app.config["DEBUG"])


if __name__ == '__main__':
    unittest.main()
