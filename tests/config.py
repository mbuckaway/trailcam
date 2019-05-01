import unittest
from webcamlib.Config import Config
import logging

class TestConfigMethods(unittest.TestCase):
    def setUp(self):
        self.configFile = Config('tests/config-test.json')

    def tearDown(self):
        self.configFile.dispose()

    def runTest(self):
        self.assertEqual('v4l', self.configFile.camera.cameratype)
        self.assertEqual('/dev/video0', self.configFile.camera.device)
        self.assertEqual(2, self.configFile.camera.delay)
        self.assertEqual('43.4873066', self.configFile.camera.latitude)
        self.assertEqual('-80.4841633', self.configFile.camera.longitude)
        self.assertEqual(400, self.configFile.camera.elevation)
        self.assertTrue(self.configFile.sensors.temperature.enabled)
        self.assertTrue(self.configFile.sensors.light.enabled)
        self.assertTrue(self.configFile.sensors.voltage.enabled)
        self.assertEqual(1440, self.configFile.image.width)
        self.assertEqual(810, self.configFile.image.height)
        self.assertEqual("/tmp/webcam.jpg", self.configFile.image.filename)
        self.assertEqual("servername", self.configFile.ftp.server)
        self.assertEqual("CONSUMER SECRET", self.configFile.twitter.consumersecret)

        self.assertTrue(self.configFile.hwmon.twilio_enabled)
        self.assertEqual('ACCOUNT_SID', self.configFile.hwmon.twilio_account_sid)
        self.assertEqual('AUTH_TOKEN', self.configFile.hwmon.twilio_auth_token)
        self.assertEqual('+12262345678', self.configFile.hwmon.twilio_phone_number)
        self.assertEqual('KW Geesecam is under voltage! Currently %%VOLTS%%V', self.configFile.hwmon.message_warning)
        self.assertEqual('KW Geesecam is dead! Currently %%VOLTS%%V. Shutting down!', self.configFile.hwmon.message_shutdown)
        self.assertEqual(1800, self.configFile.hwmon.smslimit)
        self.assertTrue(type(self.configFile.hwmon.phone_numbers) is list)
        self.assertEqual(2, len(self.configFile.hwmon.phone_numbers))
        self.assertEqual('+12262345555', self.configFile.hwmon.phone_numbers[0])
        self.assertEqual('+12262345556', self.configFile.hwmon.phone_numbers[1])

        self.assertEqual(10.0, self.configFile.hwmon.warning_voltage)
        self.assertEqual(9.1, self.configFile.hwmon.shutdown_voltage)
        self.assertEqual('/tmp/trailcamlastcheck.json', self.configFile.hwmon.timefile)

        self.assertEqual(60, self.configFile.scheduler.interval)
        self.assertEqual(3, len(self.configFile.scheduler.processes))
        process = self.configFile.scheduler.processes[0]
        self.assertTrue(process.enabled)
        self.assertEqual(1, process.count)
        self.assertEqual(3, len(process.functions))
        self.assertEqual("sensors", process.functions[0])
        self.assertEqual("senddata", process.functions[1])
        self.assertEqual("checkvalues", process.functions[2])

        process = self.configFile.scheduler.processes[1]
        self.assertFalse(process.enabled)
        self.assertEqual(5, process.count)
        self.assertEqual(3, len(process.functions))
        self.assertEqual("annotate", process.functions[0])
        self.assertEqual("photo", process.functions[1])
        self.assertEqual("ftpupload", process.functions[2])

        process = self.configFile.scheduler.processes[2]
        self.assertFalse(process.enabled)
        self.assertEqual(60, process.count)
        self.assertEqual(1, len(process.functions))
        self.assertEqual("twitterupload", process.functions[0])

        self.assertTrue(self.configFile.restapi.enabled)
        self.assertEqual(1, self.configFile.restapi.camera_id)
        self.assertEqual("http://kwgeesecam.ca", self.configFile.restapi.host)
        self.assertEqual("API_KEY", self.configFile.restapi.api_key)

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