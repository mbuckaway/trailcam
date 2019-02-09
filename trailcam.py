#!/usr/bin/python3
import os
import pygame, sys
import datetime
import time
import board
import busio
import adafruit_bmp280
import ftplib
import argparse
import json
import logging
import ephem
import math
from pathlib import PosixPath
from logging_configurator import configure_logging
from picamera import PiCamera
from PIL import Image, ImageFont, ImageDraw
import select
import v4l2capture
from twython import Twython

configure_logging()

verbose = False
ftpEnabled = True
twitterEnabled = True
sensorEnabled = True

def vprint(string):
    logging.debug(string)

def getconfig(configfile):
    with open(configfile) as json_data:
        config = json.load(json_data)
    return config

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

def tempdata(addressvalue, sea_level_pressure):
    # Create library object using our Bus I2C port
    i2c = busio.I2C(board.SCL, board.SDA)
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=addressvalue)

    # change this to match the location's pressure (hPa) at sea level
    bmp280.sea_level_pressure = sea_level_pressure
    logging.debug("Getting temperature...")
    temp = "Temp: %0.1fC " % bmp280.temperature
    pres = "Barometer: %0.1fhPa " % bmp280.pressure
    #alti = "Altitute: %0.2fm " % bmp280.altitude
    data = temp + pres
    logging.info(data)
    return data

def snapshotPiCamera(isdaytime, width, height, filename):
    with PiCamera() as camera:
        camera.resolution = (width, height)
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
            camera.capture(filename, format='jpeg', use_video_port=False)
            time.sleep(1)
            camera.capture(filename, format='jpeg', use_video_port=False)
        except:
            logging.error("Camera was unable to capture an image")

def snapshotv4l(device, width, height, filename, delay):
    logging.info("Taking photo from device: " + device)
    # Open the video device.
    video = v4l2capture.Video_device(device)

    # Suggest an image size to the device. The device may choose and
    # return another size if it doesn't support the suggested one.
    size_x, size_y = video.set_format(width, height)

    # Create a buffer to store image data in. This must be done before
    # calling 'start' if v4l2capture is compiled with libv4l2. Otherwise
    # raises IOError.
    video.create_buffers(1)

    # Start the device. This lights the LED if it's a camera that has one.
    #print("Exposure: " + str(video.get_exposure_absolute()))
    video.start()

    # Wait a little. Some cameras take a few seconds to get bright enough.
    if (delay>0):
        time.sleep(delay)

    # Send the buffer to the device.
    video.queue_all_buffers()

    # Wait for the device to fill the buffer.
    select.select((video,), (), ())

    # The rest is easy :-)
    image_data = video.read()
    video.stop()
    video.close()
    image = Image.frombytes("RGB", (size_x, size_y), image_data)
    logging.info("Saving file: " + filename)
    image.save(filename)

def annotate(filename, weather):
    base = Image.open(filename).convert('RGBA')
    txt = Image.new('RGBA', base.size, (255,255,255,0))
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 18)
    draw = ImageDraw.Draw(txt)
    pos_x = base.height - 30
    date = datetime.datetime.now().strftime("%B %d, %Y %I:%M%p")
    draw.text((10, pos_x), "Hydrocut Status (" + date + "): " + weather, font=font,fill=(255,255,255,128))
    out = Image.alpha_composite(base, txt)

    logging.info("Saving image with weather data")
    out.convert('RGB').save(filename)

def ftpfile(server, user, password, filename, remotefile):
    logging.info("Uploading file to " + server + " as " + remotefile)
    try:
        now = datetime.datetime.now()
        path = PosixPath(remotefile)
        directory = now.strftime("%Y%U")
        archivefilename = directory + "/" + path.stem + "-" + now.strftime("%Y%m%d-%H%M%S") + path.suffix
        session = ftplib.FTP(server,user,password)
        # make a new directory and don't complain if it's already there
        logging.info("Storing old image in " + directory + " as " + archivefilename)
        try:
            session.mkd(directory)
        except:
            logging.warn("Error creating directory (ignored)")
        try:
            logging.debug("Renaming " + remotefile + " to " + archivefilename)
            session.rename(remotefile, archivefilename)
        except:
            logging.error("Error archiving file")

        photo = open(filename,'rb')                  # file to send
        session.storbinary('STOR ' + remotefile, photo)     # send the file
        photo.close()                                    # close file and FTP
        session.quit()
        session.close()
        logging.info("Upload completed successfully.")
    except:
        logging.error('Failed to FTP file')

def twitterpost(filename, twitter, weather):
    logging.info("Posting to twitter...")
    try:
        #Create a copy of the Twython object with all our keys and secrets to allow easy commands.
        api = Twython(twitter['ConsumerKey'], twitter['ConsumerSecret'], twitter['AccessKey'], twitter['AccessSecret']) 
        #Using our newly created object, utilize the update_status to send in the text passed in through CMD
        photo = open(filename,'rb')                  # file to send
        response = api.upload_media(media=photo)
        api.update_status(status='Hydrocut Status: ' + weather, media_ids=[response['media_id']])
        photo.close()                                    # close file and FTP
    except:
        logging.error('Failed to Tweet the status')

parser = argparse.ArgumentParser(description='Trail Webcam utility')
parser.add_argument('-l', '--logfile', default='trailcam.log', help='logging filename')
parser.add_argument('-L', '--loglevel', default='INFO', help='logging level (default INFO)')
parser.add_argument('-c', '--config', default='config.json', help='config filename')
parser.add_argument('-f', '--ftp', action='store_false', help='disable ftp')
parser.add_argument('-t', '--twitter', action='store_false', help='disable twitter')
parser.add_argument('-s', '--sensor', action='store_false', help='disable temperator sensor')
parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')

args = parser.parse_args()

configure_logging(args.logfile, args.loglevel, True, False)

if (args.verbose):
    configure_logging(args.logfile, 'DEBUG', True, True)
    verbose = True

logging.debug('Loading config: ' + args.config)
config = getconfig(args.config)

ftpEnabled = config['ftp']['enabled']
if (args.ftp == False):
    logging.warn("FTP Disabled!")
    ftpEnabled = False

twitterEnabled = config['twitter']['enabled']
if (args.twitter == False):
    logging.warn("Twitter Disabled!")
    twitterEnabled = False

sensorEnabled = config['sensor']['enabled']
if (args.sensor == False):
    logging.warn("Sensor Disabled!")
    sensorEnabled = False

logging.debug("Camera device: " + config['camera']['device'])
logging.debug("Sensor Address: " + format(config['sensor']['address'], '#04x'))
logging.debug("Image size: " + str(config['image']['width']) + "x" + str(config['image']['height']))
logging.debug("Image file: " + config['image']['filename'])
logging.debug("Ftp Server: " + config['ftp']['server'])
logging.debug("Ftp User: " + config['ftp']['user'])

# Load the temperature data
if (sensorEnabled == True):
    weather = tempdata(config['sensor']['address'], config['sensor']['sea_level_pressure'])
else:
    weather = ''

if (config['camera']['type'] == 'pi'):
    logging.debug("Using PI camera")
    isdaytime = isdaytime(config['camera']['latitude'], config['camera']['longitude'], config['camera']['elevation'])
    logging.info("System is in day mode: " + str(isdaytime))
    snapshotPiCamera(isdaytime, config['image']['width'], config['image']['height'], config['image']['filename'])
else:    
    logging.debug("Using USB camera")
    snapshotv4l(config['camera']['device'], config['image']['width'], config['image']['height'], config['image']['filename'], config['camera']['delay'])

if (twitterEnabled):
    twitterpost(config['image']['filename'], config['twitter'], weather)

annotate(config['image']['filename'], weather)

if (ftpEnabled):
    ftpfile(config['ftp']['server'], config['ftp']['user'], config['ftp']['password'], config['image']['filename'], config['ftp']['remotefile'])












