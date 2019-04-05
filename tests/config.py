import unittest
from webcamlib.Config import Config

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
        self.assertTrue(self.configFile.temperature.enabled)
        self.assertTrue(self.configFile.lightsensor.enabled)
        self.assertTrue(self.configFile.voltagesensor.enabled)
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

        self.assertEqual(7.0, self.configFile.hwmon.warning_voltage)
        self.assertEqual(6.0, self.configFile.hwmon.shutdown_voltage)
        self.assertEqual(60, self.configFile.hwmon.check_interval)
        self.assertEqual('/tmp/voltage.xlxs', self.configFile.hwmon.datafile)
        self.assertEqual('/tmp/trailcamlastcheck.json', self.configFile.hwmon.timefile)

if __name__ == '__main__':
    unittest.main()