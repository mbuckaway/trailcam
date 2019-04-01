#!/usr/bin/env python3
import unittest
from tests.camera import TestCameraMethods
from tests.ftpfile import TestFtpFileMethods
from tests.config import TestConfigMethods
from tests.twitterpost import TestTwitterPostMethods
from tests.lightsensor import TestLightSensorMethods
from tests.temperaturesensor import TestTemperatureSensorMethods
from tests.voltagesensor import TestVoltageSensorMethods

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestConfigMethods())
    suite.addTest(TestFtpFileMethods())
    suite.addTest(TestCameraMethods())
    suite.addTest(TestTwitterPostMethods())
    suite.addTest(TestTemperatureSensorMethods())
    suite.addTest(TestVoltageSensorMethods())
    
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())