import unittest
from webcamlib.Config import Config
from webcamlib.Scheduler import SchedulerData, Process
import logging

"""
 "unit" test to make sure the Scheduler data and process class work
"""
class TestSchedulerMethods(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def runTest(self):
        schedulerData = SchedulerData()
        schedulerData.temperature = 50.0
        self.assertEqual(50.0, schedulerData.temperature)
        schedulerData.voltage = 12.0
        self.assertEqual(12.0, schedulerData.voltage)
        schedulerData.current = 222.0
        self.assertEqual(222.0, schedulerData.current)
        schedulerData.light = 1234
        self.assertEqual(1234, schedulerData.light)
        schedulerData.annotation_photo = "Welcome"
        self.assertEqual("Welcome", schedulerData.annotation_photo)
        schedulerData.annotation_twitter = "twitter"
        self.assertEqual("twitter", schedulerData.annotation_twitter)

        functions = [
            "annotate",
            "senddata",
            "photo"
        ]
        process = Process(5, 4, "Testing", functions)
        self.assertEqual("Testing", process.description)
        self.assertEqual("annotate", process.functions[0])
        self.assertEqual("senddata", process.functions[1])
        self.assertEqual("photo", process.functions[2])
        self.assertFalse(process.do_runtask)
        process.decrement_count()
        self.assertFalse(process.do_runtask)
        process.decrement_count()
        self.assertFalse(process.do_runtask)
        process.decrement_count()
        self.assertFalse(process.do_runtask)
        process.decrement_count()
        self.assertTrue(process.do_runtask)
        process.reset_count()
        self.assertFalse(process.do_runtask)
        process.decrement_count()
        self.assertFalse(process.do_runtask)


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