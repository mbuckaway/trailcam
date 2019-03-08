#!/usr/bin/env python3

from setuptools import setup

setup(name='TrailCam',
        version='1.0',
        description='Webcam with FTP and Twitter',
        author='Mark Buckaway',
        author_email='mark@buckaway.ca',
        url='http://github.com/mbuckaway/trailcam',
        packages=['trailcam'],
        entry_points = {'console_scripts': ['trailcam = trailcam.py',],},
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
            "logging_configurator": ["logging_configurator"],
        }
)
