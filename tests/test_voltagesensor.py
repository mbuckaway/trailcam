import unittest
from webcamlib.Config import Config
from webcamlib.VoltageSensor import VoltageSensor
from logging_configurator import configure_logging

"""
 "unit" test (more of a functional test) to make sure the voltage works
"""
class TestVoltageSensorMethods(unittest.TestCase):
    def setUp(self):
        configure_logging()
        self.configFile = Config('tests/config-test.json')

    def tearDown(self):
        self.configFile.dispose()

    def runTest(self):
        sensor = VoltageSensor(self.configFile.sensors.voltage)
        self.assertNotEqual(0, sensor.voltage)
        self.assertNotEqual(0, sensor.current)
        print("Voltage: " + str(sensor.voltage))
        print("Current: " + str(sensor.current))

if __name__ == '__main__':
    unittest.main()