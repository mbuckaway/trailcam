#!/usr/bin/env python3

from setuptools import setup

setup(name='TrailCam',
        version='1.0',
        description='Webcam with FTP and Twitter',
        author='Mark Buckaway',
        author_email='mark@buckaway.ca',
        url='http://github.com/mbuckaway/trailcam',
        packages=['webcamlib'],
        include_package_data=True,
        entry_points = {'console_scripts': ['trailcam = webcamlib.cli_webcam:main',],},
        requires={
            "ftplib": ["ftplib"],
            "argparse": ["argparse"],
            "json": ["json"],
            "logging": ["logging"],
            "ephem": ["ephem"],
            "pillow": ["pillow"],
            "v4l2capture": ["v4l2capture"],
            "picamera": ["picamera"],
            "twython": ["twython"],
            "unittest": ["unittest"],
            "adafruit_ina219": ["adafruit_ina219"],
        }
)
