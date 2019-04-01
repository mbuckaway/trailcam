import unittest
from webcamlib.Config import Config
from webcamlib.FtpFile import FtpFile
from logging_configurator import configure_logging

"""
 "unit" test (more of a functional test) to make sure the FTP works
"""
class TestFtpFileMethods(unittest.TestCase):
    def setUp(self):
        configure_logging()
        self.configFile = Config('tests/config-test.json', True, False)

    def tearDown(self):
        self.configFile.dispose()

    def runTest(self):
        success = True
        try:
            ftpfile = FtpFile(self.configFile.ftp, self.configFile.image)
            ftpfile.sendfile()
        except Exception as e:
            success = False
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()