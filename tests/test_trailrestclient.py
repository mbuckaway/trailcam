import unittest
from webcamlib.Config import Config
from webcamlib.FileRestClient import FileRestClient
import logging
import os

"""
 "unit" test (more of a functional test) to make sure the Sending SMS works
"""
class TestFileResetClientMethods(unittest.TestCase):
    def setUp(self):
        self.config = Config('../config.json')

    def tearDown(self):
        self.config.dispose()

    def runTest(self):
        success = True
        filename = "testfile.jpg"
        directory = "images/webcam"
        restclient = FileRestClient(self.config)
        try:
            restclient.new_file(filename, directory)
        except Exception as e:
            print('New File Test failed with exception: ' + str(e.args))
            success = False
        self.assertTrue(success)

        try:
            restclient.delete_by_name(filename, directory)
        except Exception as e:
            print('Delete Test failed with exception: ' + str(e.args))
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