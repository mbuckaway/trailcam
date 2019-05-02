import unittest
from webcamlib.Config import Config
from webcamlib.FtpFile import FtpFile
from webcamlib.Scheduler import SchedulerData
import logging

"""
 "unit" test (more of a functional test) to make sure the FTP works
"""
class TestFtpFileMethods(unittest.TestCase):
    def setUp(self):
        self.configFile = Config('../config.json', True, False)
        self.data = SchedulerData()

    def tearDown(self):
        self.configFile.dispose()

    def runTest(self):
        success = True
        try:
            ftpfile = FtpFile(self.configFile, self.data)
            ftpfile.sendfile()
        except Exception:
            success = False
            print("Test failed with error: {}".format(self.data.lasterror))
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