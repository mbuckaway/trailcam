from webcamlib.Config import Config, ConfigScheduler
import logging
import sched, time
from datetime import datetime
from logging_configurator import configure_logging

class Scheduler():
    """ Class to open a running the main code on a schedule """
    def __init__(self, scheduleconfig):
        self.scheduleconfig = scheduleconfig
        self.scheduler = sched.scheduler(time.time, time.sleep)
        now = datetime.now()
        hour = now.hour
        minute = now.minute + 1
        if (minute>59):
            hour +=1
            minute =0
        if (hour > 24):
            hour = 0
        logging.info("First action starts at " + str(hour) + ":" + str(minute))
        nextminute = datetime(now.year, now.month, now.day, hour, minute, 0)
        self.lastevent = self.scheduler.enterabs(nextminute.timestamp(), 1, self.action)
        self.count = 3

    def action(self):
        """ Method to run ever scheduler tick """
        self.lastevent = self.scheduler.enter(self.scheduleconfig.interval, 1, self.action)
        logging.debug("Running action")
        if (self.count == 0):
            self.stop()
        else:
            self.count-=1

    def run(self):
        """ Method to run the scheduler. Method never returns! """
        self.scheduler.run(blocking=True)

    def stop(self):
        """ Checks if the queue is empty, and if not, cancels it """
        logging.info("Stopping scheduler")
        if (not self.scheduler.empty()):
            self.scheduler.cancel(self.lastevent)

if __name__ == '__main__':
    configure_logging(log_level='DEBUG', stdout=True)
    config = Config('../config.json')
    scheduler = Scheduler(config.scheduler)
    scheduler.run()        