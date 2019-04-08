import unittest
from webcamlib.Config import Config
from webcamlib.ThingSpeakData import ThingSpeakData
from logging_configurator import configure_logging

"""
 "unit" test (more of a functional test) to make sure the thingspeak data is sent
"""
class TestThingSpeakDataMethods(unittest.TestCase):
    def setUp(self):
        configure_logging()
        self.config = Config('../config.json')

    def tearDown(self):
        self.config.dispose()

    def runTest(self):
        thinkspeakdata = ThingSpeakData(self.config.thingspeak)
        success = True
        try:
            thinkspeakdata.WriteData(12.0, 0.200, 21, 400)
        except Exception as e:
            print('Test failed with exception: ' + str(e.args))
            success = False
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()