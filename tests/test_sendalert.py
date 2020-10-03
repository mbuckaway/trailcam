import unittest
from webcamlib.Config import Config
from webcamlib.SendAlert import SendAlert
import logging
import os

"""
 "unit" test (more of a functional test) to make sure the Sending SMS works
"""
class TestSendSMSMethods(unittest.TestCase):
    def setUp(self):
        self.config = Config('../config.json')

    def tearDown(self):
        self.config.dispose()

    def runTest(self):
        sendalert = SendAlert(self.config.hwmon)
        success = True
        try:
            sendalert.SendWarning(7.0)
        except Exception as e:
            print('Test failed with exception: ' + str(e.args))
            success = False
        self.assertTrue(success)

        success = True
        try:
            sendalert.SendShutdown(6.0)
        except Exception as e:
            print('Test failed with exception: ' + str(e.args))
            success = False
        self.assertTrue(success)

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