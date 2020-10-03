import unittest
from webcamlib.Config import Config
from webcamlib.TrailRestClient import TrailRestClient
import logging
import os

"""
 "unit" test (more of a functional test) to make sure the Sending SMS works
"""
class TestTrailRestClientMethods(unittest.TestCase):
    def setUp(self):
        self.config = Config('tests/config-test.json')

    def tearDown(self):
        self.config.dispose()

    def runTest(self):
        restclient = TrailRestClient(self.config)
        isopen = True
        try:
            isopen = restclient.status()
        except Exception as e:
            print('status failed with exception: ' + str(e.args))
        self.assertFalse(isopen)

if __name__ == '__main__':
    root_logger = logging.getLogger('')
    # Setup logging to the screen
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] [%(name)-15.15s] [%(levelname)-7.7s] %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to logger
    root_logger.addHandler(ch)
    unittest.main()