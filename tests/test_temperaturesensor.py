import unittest
from webcamlib.Config import Config
from webcamlib.TemperatureSensor import TemperatureSensor
from logging_configurator import configure_logging

"""
 "unit" test (more of a functional test) to make sure the lightsensor works
"""
class TestTemperatureSensorMethods(unittest.TestCase):
    def setUp(self):
        configure_logging()

    def tearDown(self):
        pass

    def TestDS18B20(self):
        configFile = Config('tests/config-test-ds18b20.json')
        sensor = TemperatureSensor(configFile.sensors.temperature)
        """ No pressure reading here """
        self.assertNotEqual(0, sensor.temperature)

    def TestBMP280(self):
        configFile = Config('tests/config-test-bmp280.json')
        sensor = TemperatureSensor(configFile.sensors.temperature)
        self.assertNotEqual(0, sensor.pressure)
        self.assertNotEqual(0, sensor.temperature)

    def TestMP3115A2(self):
        configFile = Config('tests/config-test-mp3115a2.json')
        sensor = TemperatureSensor(configFile.sensors.temperature)
        self.assertNotEqual(0, sensor.pressure)
        self.assertNotEqual(0, sensor.temperature)

    def runTest(self):
        self.TestDS18B20()
        self.TestBMP280()
        self.TestMP3115A2()

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