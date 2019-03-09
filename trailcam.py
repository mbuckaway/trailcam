#!/usr/bin/env python3
import os
import sys
import datetime
import time
# Should figure out how to optionally load these based on config
import ftplib
import argparse
import json
from pathlib import PosixPath
import logging
from logging_configurator import configure_logging
from twython import Twython
from Exceptions import ConfigError, DeviceError
from Config import Config, ConfigTemperature, ConfigAnnotate
from TemperatureSensor import TemperatureSensor
from LightSensor import LightSensor
from Annotate import Annotate
from Camera import Camera

def ftpmkdir(session, directory):
    path = PosixPath(directory)
    parts = path.parts
    length = len(parts)-1
    i = 0
    root = parts[0]
    while (i < length)  :
        search = parts[i+1]
        newroot = PosixPath(root).joinpath(search).as_posix()
        dirlist = session.nlst(root)
        if search not in dirlist : #check if 'foo' exist inside 'www'
            session.mkd(newroot) #Create a new directory called foo on the server.
        i=i+1
        root = newroot

def ftpfile(ftpconfig, imageconfig):
    if (ftpconfig.enabled):
        logging.info("Uploading file to " + ftpconfig.server + " as " + ftpconfig.remotefile)
        try:
            now = datetime.datetime.now()
            remotepath = PosixPath(ftpconfig.remotefile)
            archivepath = PosixPath(archivedir).joinpath(now.strftime("%Y%m/%d")).as_posix()
            archivefilename =  PosixPath(archivepath).joinpath(remotepath.stem + "-" + now.strftime("%Y%m%d-%H%M%S") + remotepath.suffix).as_posix()
            logging.debug("Remote file: " + ftpconfig.remotefile)
            logging.debug("Archive path: " + archivepath)
            logging.debug("Archive file: " + archivefilename)
            session = ftplib.FTP(ftpconfig.server,ftpconfig.user,ftpconfig.password)
            # make a new directory and don't complain if it's already there
            logging.info("Storing old image in " + archivefilename)
            try:
                ftpmkdir(session, archivepath)
                logging.debug("Renaming " + ftpconfig.remotefile + " to " + archivefilename)
                session.rename(ftpconfig.remotefile, archivefilename)
            except Exception as e:
                logging.error("Error archiving file: " + str(e.args))

            photo = open(imageconfig.filename,'rb')                  # file to send
            session.storbinary('STOR ' + remotefile, photo)     # send the file
            photo.close()                                    # close file and FTP
            session.quit()
            session.close()
            logging.info("Upload completed successfully.")
        except NameError as e:
            logging.error('Failed to FTP file: NameError in script: ' + str(e.args))
        except Exception as e:
            logging.error('Failed to FTP file: ' + str(e.args))

def twitterpost(filename, twitterconfig, annotation):
    if (twitterconfig.enabled):
        logging.info("Posting to twitter...")
        try:
            #Create a copy of the Twython object with all our keys and secrets to allow easy commands.
            api = Twython(twitterconfig.consumerkey, twitterconfig.consumersecret, twitterconfig.accesskey, twitterconfig.accesssecret) 
            #Using our newly created object, utilize the update_status to send in the text passed in through CMD
            photo = open(filename,'rb')                  # file to send
            response = api.upload_media(media=photo)
            api.update_status(status=annotation, media_ids=[response['media_id']])
            photo.close()                                    # close file and FTP
        except Exception as e:
            logging.error('Failed to Tweet the status: ' + str(e.args))

def main():
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

    twitterpost(config.image.filename, config.twitter, annotate.annotation_twitter)
    ftpfile(config.ftp, config.image)

if __name__ == '__main__':
    try:
        configure_logging()
        main()
    except Exception as e:
        logging.error("Unhandled exception caught: " + str(e.args))










