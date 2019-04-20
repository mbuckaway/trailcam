import unittest
from webcamlib.Config import Config
from webcamlib.Camera import Camera
from logging_configurator import configure_logging

"""
 "unit" test (more of a functional test) to make sure the camera works
"""
class TestCameraMethods(unittest.TestCase):
    def setUp(self):
        configure_logging()
        self.configFile = Config('tests/config-test.json', True, False)

    def tearDown(self):
        self.configFile.dispose()

    def runTest(self):
        success = True
        try:
            camera = Camera(self.configFile.camera, self.configFile.image, self.configFile.led, 0)
            camera.SnapPhoto()
        except Exception as e:
            success = False
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()