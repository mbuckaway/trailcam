# Trailcam

This program is a simple Webcam Utility for a Raspberry PI. Currently, the system runs on a PI Zero W and is connected to a 4G modem via WIFI, connected to a 12V to USB power supply connected to a 12V car battery. The entire thing was put in a waterproof box and put into the forest at the Hydrocut (http://thehydrocut.ca)

The utility is meant to be run on a cron job and can post to a ftp site and a twitter account. It also has the ability to read temperature and pressure from the BMP280 temperature sensor on the I2C bus. All things are configurable in the config.json config file.

This utility is work in progress. Features to be added:
- voltage and current sensors to monitor the state of the 12v battery system (possible current sensor on the solar charge controller)
- LED on a GPIO pin to len people know when a photo is about to be taken
- relay controller to control a 12V floodlight for night time shots (currently, night shots produce nothing)
- AI image processing to detect when the scene is empty, has a hiker, or has a mountain bike (or number  of mountain bikes).


# Linux Dependancies

The following packages are required:
```
libv4l-dev
```

This is only required for Video for Linux support. As of Debian 10, the v2l python package does not work.

# Kernel Module installation

Rather than use Python modules that bit bang on the I2C and W1 buses, I've elected to use Linux supplied kernel drivers to support the devices for the project. This means that the drivers expose the devices in the /sys/bus filesystem enabling simple python code to read standard text files to get sensor information.

This also means that the kernel source tree is required to build the modules. Luckily, actually building the entire kernel is not required, only building the required modules. THe rpisource utility helps get the correct kernel source from the github report. The rpisource app can be found here:

rpisource: https://github.com/notro/rpi-source

The kernel modules themselves can be be built by reading:

https://github.com/notro/rpi-source/wiki/Examples-on-how-to-build-various-modules

However, changes to the kernel seem to make building a single drive a pain. The SUBDIRS item in the instructions no longer works. This website gives a better way:

http://blog.vmsplice.net/2018/01/how-to-modify-kernel-modules-without.html

Basically, edit the .config to enable the required modules, and then run:

```bash
make prepare
make modules_prepare
make M=drivers/iio/light modules
make M=drivers/iio/light modules_install
```

Otherwise, it might try to build all the modules...and on a RPi Zero, this will take days.

For this project, the following devices are supported:
i2c:
bh1750 - light sensor
bmp280 - temp/pressure sensor (and in bmXX80 range should work)
mpl3115a2 - temp/pressure sensor

1wire:
w1-therm - ds18b20 temperature sensor

hwmod:
ina2xxx - voltage sensor

Additional sensors can be added by extending the LightSensor.py and TemperatureSensor.py classes.
