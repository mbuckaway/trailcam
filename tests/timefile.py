import unittest
from webcamlib.Config import Config
from webcamlib.TimeFile import TimeFile
from logging_configurator import configure_logging
from datetime import datetime

import os

"""
 "unit" test (more of a functional test) to make sure the TimeFile Serialized/Deserialize save to file methods*
"""
class TestTimeFileMethods(unittest.TestCase):
    def setUp(self):
        configure_logging()
        self.config = Config('config-test.json')

    def tearDown(self):
        self.config.dispose()

    def runTest(self):
        timefile = TimeFile(self.config.hwmon)
        timefile.lastrundatetime = datetime(2018,1,1,1,1,1)
        timefile.lastruntime = datetime(2018,2,2,2,2,2)
        success = True
        try:
            timefile.UpdateData()
        except Exception as e:
            print('Test failed with exception: ' + str(e.args))
            success = False
        self.assertTrue(success)

        success = True
        try:
            timefile.ReadData()
        except Exception as e:
            print('Test failed with exception: ' + str(e.args))
            success = False
        self.assertTrue(success)
        self.assertEqual(datetime(2018,1,1,1,1,1), timefile.lastrundatetime)
        self.assertEqual(datetime(2018,2,2,2,2,2), timefile.lastruntime)

if __name__ == '__main__':
    unittest.main()