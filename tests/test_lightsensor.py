import unittest
from webcamlib.Config import Config
from webcamlib.LightSensor import LightSensor
import logging

"""
 "unit" test (more of a functional test) to make sure the lightsensor works
"""
class TestLightSensorMethods(unittest.TestCase):
    def setUp(self):
        self.configFile = Config('tests/config-test-bh1750.json')

    def tearDown(self):
        self.configFile.dispose()

    def runTest(self):
        sensor = LightSensor(self.configFile.sensors.light)
        self.assertNotEqual(0, sensor.lightlevel)

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