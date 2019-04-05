import unittest
from webcamlib.Config import Config
from webcamlib.SendAlert import SendAlert
from logging_configurator import configure_logging

import os

"""
 "unit" test (more of a functional test) to make sure the Sending SMS works
"""
class TestSendSMSMethods(unittest.TestCase):
    def setUp(self):
        configure_logging()
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
    unittest.main()