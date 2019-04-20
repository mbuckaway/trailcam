import unittest
from webcamlib.Config import Config
from webcamlib.TwitterPost import TwitterPost
from logging_configurator import configure_logging

"""
 "unit" test (more of a functional test) to make sure the FTP works
"""
class TestTwitterPostMethods(unittest.TestCase):
    def setUp(self):
        configure_logging()
        self.config = Config('tests/config-test.json', True, False)

    def tearDown(self):
        self.config.dispose()

    def runTest(self):
        success = True
        try:
            twitter = TwitterPost(self.config.image.filename, self.config.twitter, 'This is a test')
            twitter.post()
        except Exception as e:
            success = False
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()