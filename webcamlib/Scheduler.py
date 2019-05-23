from webcamlib.Config import Config, ConfigScheduler
from webcamlib.Exceptions import InvalidFunctionError
from webcamlib.Annotate import Annotate
from webcamlib.TemperatureSensor import TemperatureSensor
from webcamlib.VoltageSensor import VoltageSensor
from webcamlib.LightSensor import LightSensor
from webcamlib.ThingSpeakData import ThingSpeakData
from webcamlib.SendAlert import SendAlert
from webcamlib.Camera import Camera
from webcamlib.FtpFile import FtpFile
from webcamlib.TwitterPost import TwitterPost

import logging
import sched, time
import sys
from datetime import datetime
import signal
import subprocess

class Process:
    """
    Class to hold the process data:
        ticks - number of tick before a process is run
        count - current tick count
        description - describes the task
        functions - functions to run
    """
    def __init__(self, ticks, count, decription, functions):
        self.logger = logging.getLogger('process')
        self.property_ticks = ticks
        self.property_count = count
        self.property_functions = functions
        self.property_description = decription
        self.logger.debug("New Process starting at " + str(ticks) + " with count " + str(count) + " and functions " + str(functions))

    def decrement_count(self):
        if (self.property_count != 0):
            self.property_count-=1
        self.logger.debug("{} process {} ticks remaining".format(self.property_description, self.property_count))

    def reset_count(self):
        self.property_count=self.property_ticks-1
        if (self.property_ticks<0):
            self.property_ticks=0

    @property
    def description (self):
        return self.property_description 

    @property
    def functions(self):
        return self.property_functions

    @property
    def do_runtask(self):
        return (self.property_count==0)

class SchedulerData:
    """
    Data storage class. Holds data for the scheduler that is passed around to each of the processes.
    """    
    def __init__(self):
        self.property_temperature = 0.0
        self.property_pressure = 0.0
        self.property_voltage = 0.0
        self.property_current = 0.0
        self.property_light = 400
        self.property_annotation_photo = "This is a test"
        self.property_annotation_twitter = "This is a test"
        self.property_error = []

    @property
    def temperature(self):
        return self.property_temperature

    @temperature.setter
    def temperature(self, value):
        self.property_temperature = value

    @property
    def pressure(self):
        return (self.property_pressure)

    @pressure.setter
    def pressure(self, value):
        self.property_pressure = value

    @property
    def voltage(self):
        return self.property_voltage

    @voltage.setter
    def voltage(self, value):
        self.property_voltage = value

    @property
    def current(self):
        return self.property_current

    @current.setter
    def current(self, value):
        self.property_current = value

    @property
    def light(self):
        return self.property_light

    @light.setter
    def light(self, value):
        self.property_light = value

    @property
    def annotation_photo(self):
        return self.property_annotation_photo

    @annotation_photo.setter
    def annotation_photo(self, value):
        self.property_annotation_photo = value

    @property
    def annotation_twitter(self):
        return self.property_annotation_twitter

    @annotation_twitter.setter
    def annotation_twitter(self, value):
        self.property_annotation_twitter = value

    @property
    def haserror(self):
        return len(self.property_error)>0

    def clearerror(self):
        self.property_error.clear()

    @property
    def lasterror(self):
        sep = ": "
        errorstr = sep.join(self.property_error)
        return errorstr

    @lasterror.setter
    def lasterror(self, value):
        self.property_error.append(value)

class Scheduler:
    """
    Class to run processes on a schedule. The current scheduler limits events to one hour cycles in that the max interval length
    is one hour. Most actions happen every minute, every five minutes, or every hour for our purposes. This is a "cheesy scheduler".
    It is a quick hack and this scheduler may be replaced at some point if more than items per hour are required.
    """
    def __init__(self, config):
        self.logger = logging.getLogger('schedule')
        self.config = config
        self.data = SchedulerData()
        self.functions = {
            'sensors': self.sensors,
            'senddata': self.senddata,
            'checkvalues': self.checkvalues,
            'annotate': self.annotate,
            'photo': self.photo,
            'ftpupload': self.ftpupload,
            'twitterupload': self.twitterupload
        }
        self.SIGNALS_TO_NAMES_DICT = dict((getattr(signal, n), n) \
            for n in dir(signal) if n.startswith('SIG') and '_' not in n )

        self.processes = []
        # Calculate the number of ticks until the next run of
        # each process based on the configuration
        self.ticksperhour = int(3600/self.config.scheduler.interval)
        self.intervalsperminute = int(60/self.config.scheduler.interval)
        # Check that the actions are valid
        now = datetime.now()
        minute = now.minute
        self.logger.debug("Time now is {0}:{1}".format(now.hour, now.minute))
        self.logger.debug("Intervals per minute: {0}".format(self.intervalsperminute))
        self.logger.debug("Ticks per hour: {0}".format(self.ticksperhour))
        self.lastevent = 0
        for process in self.config.scheduler.processes:
            if (process.enabled):
                for function in process.functions:
                    if (function not in self.functions):
                        raise InvalidFunctionError(function)
                # Special case. count is same as intervals per min. No calculation needed.
                if (process.count == self.intervalsperminute):
                    current_count = 0
                    process_ticks_perhour = self.intervalsperminute*60
                elif (process.count == self.ticksperhour):
                    # if we run once per hour, then the count is the min number
                    current_count = self.ticksperhour - minute
                else:
                    process_ticks_perhour = int(self.ticksperhour/process.count)
                    current_count = int(minute%process.count)
                    #if (current_ticks<0):
                    #    current_ticks = 0

                self.logger.debug("---")
                self.logger.debug("process_ticks_perhour {}".format(process_ticks_perhour))
                self.logger.debug("current_count " + str(current_count))
                self.logger.debug("process.ticks " + str(process.count))
                
                self.processes.append(Process(process.count, current_count, process.description, process.functions))                

        self.action()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        now = datetime.now()
        hour = now.hour
        minute = now.minute + 1
        if (minute>59):
            hour +=1
            minute =0
        if (hour > 24):
            hour = 0
        self.logger.info("First action starts at " + str(hour) + ":" + str(minute))
        nextminute = datetime(now.year, now.month, now.day, hour, minute, 0)
        self.lastevent = self.scheduler.enterabs(nextminute.timestamp(), 1, self.action)

    def action(self):
        """ Method to run ever scheduler tick """
        if (self.lastevent):
            self.lastevent = self.scheduler.enter(self.config.scheduler.interval, 1, self.action)
        now = datetime.now()
        self.logger.debug("Running action at {}:{}".format(now.hour, now.minute))
        for process in self.processes:
            if (process.do_runtask):
                process.reset_count()
                self.logger.info("Running: {}".format(process.description))
                for function in process.functions:
                    self._run_function(function)
            else:
                process.decrement_count()

    def _run_function(self, function):
        if (function in self.functions):
            self.logger.info("Running {0}".format(function))
            try:
                self.functions[function]()
            except Exception as e:
                self.logger.exception("Exception running function: %s", e)
        else:
            self.logger.error("Function {} does not exist!".format(function))

    def _receive_signal(self, signum, stack):
        if signum in [1,2,3,15]:
            self.logger.warn('Caught signal %s (%s), exiting.' % (self.SIGNALS_TO_NAMES_DICT[signum], str(signum)))
            self.stop()
            sys.exit()
        else:
            self.logger.warn('Caught signal %s (%s), ignoring.' % (self.SIGNALS_TO_NAMES_DICT[signum], str(signum)))

    def run(self):
        """ Method to run the scheduler. Method never returns! """
        signal.signal(signal.SIGINT, self._receive_signal)
        signal.signal(signal.SIGTERM, self._receive_signal)
        signal.signal(signal.SIGHUP, self._receive_signal)

        self.scheduler.run(blocking=True)

    def stop(self):
        """ Checks if the queue is empty, and if not, cancels it """
        self.logger.info("Stopping scheduler")
        self.scheduler.cancel(self.lastevent)
        if (not self.scheduler.empty()):
            self.logger.info("Scheduler empty scheduler queue")
            for event in self.scheduler.queue:
                self.scheduler.cancel(event)


    def sensors(self):
        logging.debug("Getting sensor data...")
        temperaturesensor = TemperatureSensor(self.config.sensors.temperature)
        self.data.temperature = temperaturesensor.temperature
        self.data.pressure = temperaturesensor.pressure
        logging.info("Temperature data: {}C".format(self.data.temperature))
        logging.info("Pressure data: {}hPa".format(self.data.pressure))

        lightsensor = LightSensor(self.config.sensors.light)
        self.data.light = lightsensor.lightlevel
        logging.info("Light data: {}Lux".format(self.data.light))

        voltagesensor = VoltageSensor(self.config.sensors.voltage)
        self.data.voltage = voltagesensor.voltage
        self.data.current = voltagesensor.current
        logging.info("Voltage data: {}V {}mA".format(self.data.voltage, self.data.current))

    def senddata(self):
        thingspeakdata = ThingSpeakData(self.config, self.data)
        thingspeakdata.WriteData()

    def checkvalues(self):
        """
        Check if the voltage is too low. if so, send a text msg and shutdown the system!
        However, only do this IF the voltage is more then 0 and we are enabled
        """
        if (self.config.sensors.voltage.enabled and 
            (self.data.voltage > 0) and 
            (self.data.voltage < self.config.hwmon.shutdown_voltage)):
            self.logger.warn("Supply voltage below shutdown level! ({}V)".format(self.data.voltage))
            sendalert = SendAlert(self.config.hwmon)
            sendalert.SendShutdown(self.data.voltage)
            if (self.config.hwmon.shutdown_enabled):
                self.logger.warn("Forcing system to halt and then we exit!")
                # This will fail if we are not root, but....
                subprocess.call("/sbin/halt", shell=False)
                self.stop()
                sys.exit()
        else:
            self.logger.debug("Voltage values acceptable")

    def annotate(self):
        annotate = Annotate(self.config.annotate, self.data)
        annotate.Annotate()

    def photo(self):
        # Check if the light sensor is enabled, and the light level is too low. if so, no photo.
        if ((not self.config.sensors.light.enabled) or (self.config.sensors.light.enabled and self.data.light>30)):
            camera = Camera(self.config, self.data)
            camera.SnapPhoto()
            camera.AnnotateImage()
        else:
            self.logger.warn("Skipping photo due to low light level")

    def ftpupload(self):
        if ((not self.config.sensors.light.enabled) or (self.config.sensors.light.enabled and self.data.light>30)):
            ftpfile = FtpFile(self.config, self.data)
            ftpfile.sendfile()
        else:
            self.logger.warn("Skipping photo due to low light level")

    def twitterupload(self):
        if ((not self.config.sensors.light.enabled) or (self.config.sensors.light.enabled and self.data.light>30)):
            twitterpost = TwitterPost(self.config, self.data)
            twitterpost.post()
        else:
            self.logger.warn("Skipping twitter due to low light level")

if __name__ == '__main__':
    # Setup logging to the screen only for testing
    root_logger = logging.getLogger('')
    root_logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(name)-10.10s] [%(levelname)-7.7s] %(message)s')
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)

    try:
        config = Config('../config.json')
        scheduler = Scheduler(config)
        scheduler.run()
    except Exception as e:
        root_logger.exception("Error: %s", e)
