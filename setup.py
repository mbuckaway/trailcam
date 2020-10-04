#!/usr/bin/env python3

from setuptools import setup

setup(name='TrailCam',
        version='1.3',
        description='Webcam Library with FTP and Twitter',
        author='Mark Buckaway',
        author_email='mark@buckaway.ca',
        url='http://github.com/mbuckaway/trailcam',
        packages=['webcamlib'],
        include_package_data=True,
        entry_points = {'console_scripts': ['trailcam = webcamlib.cli_webcam:main']},
        install_requires=[
            "ephem",
            "pillow",
            "picamera",
            "twython",
            "adafruit-circuitpython-ina219",
            "twilio",
            "python-daemon",
            "requests"
        ]
)
