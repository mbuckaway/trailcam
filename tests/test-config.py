import unittest
from webcamlib.Config import Config

class TestConfigMethods(unittest.TestCase):
    def setUp(self):
        self.configFile = Config('config-test.json')

    def tearDown(self):
        self.configFile.dispose()

    def test_config(self):
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

if __name__ == '__main__':
    unittest.main()