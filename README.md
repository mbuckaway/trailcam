# Trailcam

This program is a simple Webcam Utility for a Raspberry PI. Currently, the system runs on a PI Zero W and is connected to a 4G modem via WIFI, connected to a 12V to USB power supply connected to a 12V car battery. The entire thing was put in a waterproof box and put into the forest at the Hydrocut (http://thehydrocut.ca)

The utility is meant to be run on a cron job and can post to a ftp site and a twitter account. It also has the ability to read temperature and pressure from the BMP280 temperature sensor on the I2C bus. All things are configurable in the config.json config file.

This utility is work in progress. Features to be added:
- voltage and current sensors to monitor the state of the 12v battery system (possible current sensor on the solar charge controller)
- LED on a GPIO pin to len people know when a photo is about to be taken
- relay controller to control a 12V floodlight for night time shots (currently, night shots produce nothing)
- AI image processing to detect when the scene is empty, has a hiker, or has a mountain bike (or number  of mountain bikes).

