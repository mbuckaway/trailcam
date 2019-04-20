#!/usr/bin/env python3
import argparse
import logging
from webcamlib.ConfigureLogging import logging_setup
from webcamlib.Exceptions import ConfigError, DeviceError
from webcamlib.Config import Config
from webcamlib.TemperatureSensor import TemperatureSensor
from webcamlib.LightSensor import LightSensor
from webcamlib.Annotate import Annotate
from webcamlib.Camera import Camera
from webcamlib.FtpFile import FtpFile
from webcamlib.TwitterPost import TwitterPost
from webcamlib.Scheduler import Scheduler
import logging
from daemon import DaemonContext

def main_loop(config):
    try:
        scheduler = Scheduler(config)
        scheduler.run()
    except Exception as e:
        logging.exception("Error: %s", e)
        exit(1)

def main():
    parser = argparse.ArgumentParser(description='Trail Webcam utility')
    parser.add_argument('-L', '--loglevel', default='INFO', help='logging level (default INFO)')
    parser.add_argument('-c', '--config', default='config.json', help='config filename')
    parser.add_argument('-f', '--ftp', action='store_false', help='disable ftp')
    parser.add_argument('-t', '--twitter', action='store_false', help='disable twitter')
    parser.add_argument('-F', '--foreground', action='store_false', help='run in foreground')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    parser.add_argument('-T', '--testmode', action='store_true', help='test mode (run in foreground, twitter off, local logfile')
    parser.add_argument('-l', '--logfile', default='/var/log/trailcam.log', help='logging filename')
    parser.add_argument('-p', '--pidfile', default='/var/run/trailcam.pid', help='pidfile to use')

    # Defaults for testing
    args = parser.parse_args()
    #args.testmode = True
    if (args.testmode):
        args.foreground = True
        args.twitter = True
        args.logfile = "trailcam.log"
        args.verbose = True
        print("Running in test mode...")

    if (args.verbose):
        logging_setup(args.logfile, 'DEBUG', True, True)
    else:
        logging_setup(args.logfile, args.loglevel, True, False)

    logging.debug('Loading config: ' + args.config)
    try:
        config = Config(args.config, args.ftp, args.twitter)
    except Exception as e:
        logging.exception("Error: %s", e)
        exit(1)

    if (args.foreground):
        main_loop(config)
    else:
        try:
            with DaemonContext(pidfile=args.pidfile):
                main_loop(config)
        except Exception as e:
            logging.exception('Error creating daemon: %s', e)
            exit(1)

if __name__ == '__main__':
        main()










