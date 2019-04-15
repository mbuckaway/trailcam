#!/usr/bin/env python3
import unittest
import logging
import logging.handlers
from tests.camera import TestCameraMethods
from tests.ftpfile import TestFtpFileMethods
from tests.config import TestConfigMethods
from tests.twitterpost import TestTwitterPostMethods
from tests.lightsensor import TestLightSensorMethods
from tests.temperaturesensor import TestTemperatureSensorMethods
from tests.voltagesensor import TestVoltageSensorMethods
from tests.scheduler import TestSchedulerMethods

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestConfigMethods())
    suite.addTest(TestFtpFileMethods())
    suite.addTest(TestCameraMethods())
    suite.addTest(TestTwitterPostMethods())
    suite.addTest(TestTemperatureSensorMethods())
    suite.addTest(TestVoltageSensorMethods())
    suite.addTest(TestSchedulerMethods())
    
    return suite

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

    fh = logging.FileHandler('test-suite.log')
    fh.setLevel(logging.DEBUG)
    root_logger.addHandler(fh)


    runner = unittest.TextTestRunner()
    runner.run(suite())