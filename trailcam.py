#!/usr/bin/env python3
import os
import v4l2capture
import sys
import datetime
import time
# Should figure out how to optionally load these based on config
import ftplib
import argparse
import json
import logging
import ephem
import math
from PIL import Image, ImageFont, ImageDraw
from pathlib import PosixPath
from logging_configurator import configure_logging
from picamera import PiCamera
import select
from twython import Twython
from Exceptions import ConfigError, DeviceError
from Config import Config, ConfigTemperature, ConfigAnnotate
from TemperatureSensor import TemperatureSensor
from LightSensor import LightSensor
from Annotate import Annotate

configure_logging()

def isdaytime(lat, logi, elevation):
    sun = ephem.Sun()
    observer = ephem.Observer()
    #  Define your coordinates here
    observer.lat, observer.lon, observer.elevation = lat, logi, elevation
    # Set the time (UTC) here
    observer.date = datetime.datetime.utcnow()
    sun.compute(observer)
    current_sun_alt = sun.alt*180/math.pi
    result = True
    # If the sun is -6 or greater, we are nightime
    if (current_sun_alt<-6):
        result = False
    return result

def snapshotPiCamera(isdaytime, cameraconfig):
    with PiCamera() as camera:
        camera.resolution = (cameraconfig.width, cameraconfig.height)
        camera.awb_mode = 'auto'
        camera.rotation = 180
        camera.exif_tags['IFD0.Copyright'] = 'Copyright (c) 2019 Waterloo Cycling Club'
        camera.exif_tags['EXIF.UserComment'] = "Hydrocut Web Cam"
        # Get the time and see if we should be using night mode
        if isdaytime:
            #camera.exposure_mode = 'beach'
            camera.iso = 100
        else:
            #camera.exposure_mode = 'nightpreview'
            camera.iso = 1200
            camera.brightness = 60
        try:
            time.sleep(2)
            camera.capture(cameraconfig.filename, format='jpeg', use_video_port=False)
            time.sleep(1)
            camera.capture(cameraconfig.filename, format='jpeg', use_video_port=False)
        except:
            logging.error("Camera was unable to capture an image")

def snapshotv4l(cameraconfig, imageconfig):
    logging.info("Taking photo from device: " + cameraconfig.device)
    # Open the video device.
    video = v4l2capture.Video_device(cameraconfig.device)

    # Suggest an image size to the device. The device may choose and
    # return another size if it doesn't support the suggested one.
    size_x, size_y = video.set_format(imageconfig.width, imageconfig.height)

    # Create a buffer to store image data in. This must be done before
    # calling 'start' if v4l2capture is compiled with libv4l2. Otherwise
    # raises IOError.
    video.create_buffers(1)

    # Start the device. This lights the LED if it's a camera that has one.
    #print("Exposure: " + str(video.get_exposure_absolute()))
    video.start()

    # Wait a little. Some cameras take a few seconds to get bright enough.
    if (cameraconfig.delay>0):
        time.sleep(cameraconfig.delay)

    # Send the buffer to the device.
    video.queue_all_buffers()

    # Wait for the device to fill the buffer.
    select.select((video,), (), ())

    # The rest is easy :-)
    image_data = video.read()
    video.stop()
    video.close()
    image = Image.frombytes("RGB", (size_x, size_y), image_data)
    logging.info("Saving file: " + imageconfig.filename)
    image.save(imageconfig.filename)

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
    config = Config(args.config, args)

    annotate = Annotate(config.annotate, config.image, config.temperature, config.lightsensor)
    annotate.ReadSensors()

    if (config.camera.cameratype == 'pi'):
        logging.debug("Using PI camera")
        isdaytime = isdaytime(config.camera.latitude, config.camera.longitude, config.camera.elevation)
        logging.info("System is in day mode: " + str(isdaytime))
        snapshotPiCamera(isdaytime, config.camera)
    else:    
        logging.debug("Using USB camera")
        snapshotv4l(config.camera, config.image)

    annotate.UpdateImage()

    twitterpost(config.image.filename, config.twitter, annotate.annotation_twitter)
    ftpfile(config.ftp, config.image)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error("Unhandled exception caught: " + str(e.args))










