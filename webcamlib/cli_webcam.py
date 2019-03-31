#!/usr/bin/env python3
import argparse
import logging
from logging_configurator import configure_logging
from webcamlib.Exceptions import ConfigError, DeviceError
from webcamlib.Config import Config
from webcamlib.TemperatureSensor import TemperatureSensor
from webcamlib.LightSensor import LightSensor
from webcamlib.Annotate import Annotate
from webcamlib.Camera import Camera
from webcamlib.FtpFile import FtpFile
from webcamlib.TwitterPost import TwitterPost

def main(prog_name):
    parser = argparse.ArgumentParser(description='Trail Webcam utility')
    parser.add_argument('-l', '--logfile', default='trailcam.log', help='logging filename')
    parser.add_argument('-L', '--loglevel', default='INFO', help='logging level (default INFO)')
    parser.add_argument('-c', '--config', default='config.json', help='config filename')
    parser.add_argument('-f', '--ftp', action='store_false', help='disable ftp')
    parser.add_argument('-t', '--twitter', action='store_false', help='disable twitter')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')

    args = parser.parse_args()

    configure_logging(args.logfile, args.loglevel, True, False)

    if (args.verbose):
        configure_logging(args.logfile, 'DEBUG', True, True)

    logging.debug('Loading config: ' + args.config)
    config = Config(args.config, args.ftp, args.twitter)

    annotate = Annotate(config.annotate, config.image, config.temperature, config.lightsensor)
    annotate.ReadSensors()

    camera = Camera(config.camera, config.image, config.led, annotate.light_level)
    camera.SnapPhoto()

    annotate.UpdateImage()

    twitterpost = TwitterPost(config.image.filename, config.twitter, annotate.annotation_twitter)
    twitterpost.post()

    ftpfile = FtpFile(config.ftp, config.image)
    ftpfile.sendfile()

if __name__ == '__main__':
    try:
        configure_logging()
        main("cli_webcam")
    except Exception as e:
        logging.error("Unhandled exception caught: " + str(e.args))










