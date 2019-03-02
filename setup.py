#!/usr/bin/env python

from distutils.core import setup

setup(name='TrailCam',
      version='1.0',
      description='Webcam with FTP and Twitter',
      author='Mark Buckaway',
      author_email='mark@buckaway.ca',
      url='http://github.com/mbuckaway/trailcam',
      packages=['trailcam'],
      requires={
          "adafruit_bmp280": ["adafruit_bmp280"],
          "ftplib": ["ftplib"],
          "argparse": ["argparse"],
          "json": ["json"],
          "loggin": ["logging"],
          "ephem": ["ephem"],
          "pillow": ["pillow"],
          "v4l2capture": ["v4l2capture"],
          "picamera": ["picamera"],
          "twython": ["twython"],
          "logging_configurator": ["logging_configurator"],
      }
)
