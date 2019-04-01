import unittest
from webcamlib.Config import Config
from webcamlib.LightSensor import LightSensor
from logging_configurator import configure_logging

"""
 "unit" test (more of a functional test) to make sure the lightsensor works
"""
class TestLightSensorMethods(unittest.TestCase):
    def setUp(self):
        configure_logging()
        self.configFile = Config('tests/config-test-bh1750.json')

    def tearDown(self):
        self.configFile.dispose()

    def runTest(self):
        sensor = LightSensor(self.configFile.lightsensor)
        self.assertNotEqual(0, sensor.lightlevel)

if __name__ == '__main__':
    unittest.main()