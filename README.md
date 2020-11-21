# Trailcam

This program is a simple Webcam Utility for a Raspberry PI. Currently, the system runs on a PI Zero W and is connected to a 4G modem via WIFI, connected to a 24V solar charge systemt. The device is current running as security camera at the Hydrocut (http://thehydrocut.ca) mountain bike trails as part of the Trail Monitoring System.

The utility reads a 1 Wire Temperature sensor, light sensor, and voltage/current sensor and uploads the data to Thingspeak. Photos are captured and stored on the SDCARD for later retrieval. Uploading by FTP us also possible. All things are configurable in the config.yml config file.

This project will be depreciated in the future and replaced with an ESP32 device. It is kinda silly to run a complete linux OS to run one Python script...but the was the original design.

# Linux Dependancies for Video for Linux

The python code can support either the picamera or v4l. Additional packages are required for the python code to work.

```
sudo apt install libv4l-dev
```

As of RPi based on Debian 10, the v2l python package does not compile and some work may be required to get it to work again. Currently, the picamera is recommended.

# Kernel Module installation

Rather than use Python modules that bit bang on the I2C and W1 buses, I've elected to use Linux supplied kernel drivers to support the devices for the project. This means that the drivers expose the devices in the /sys/bus filesystem enabling simple python code to read standard text files to get sensor information.

This also means that the kernel source tree is required to build the modules. Luckily, actually building the entire kernel is not required, only building the required modules. THe rpisource utility helps get the correct kernel source from the github report. The rpisource app can be found here:

rpisource: https://github.com/notro/rpi-source

The rpisource docs seem to want you to install it as root. I suggest you do not. Use your own home directory. That is, run rpisource from your home directory and your linux source will be stored there. Additionally, for the Linux kernel 5.x, the directions are wrong. Substitute M= anywhere the above refers to SUBDIRS= (simular in the directions below). Otherwise, you will be waiting days for the kernel to re-compile.

The kernel modules themselves can be be built by reading:

https://github.com/notro/rpi-source/wiki/Examples-on-how-to-build-various-modules

Basically, once the kernel source is installed:
* cd $HOME/linux
* Run make menuconfig to enable the required drivers. The bh1750 is disabled by default. Most of the rest are already enabled.
* Run: make M=drivers/iio/light modules
* Run: sudo make M=drivers/iio/light modules_install
* Run: make M=drivers/hwmon modules
* Run: sudo make M=drivers/hwmon modules_install
* Run: make M=drivers/w1 modules
* Run: sudo make M=drivers/w1 modules_install
* Run: depmod -a

And because the kernel changes on updates, you will have to run the above any time apt upgrade is run and the kernel gets updated.

For this project, the following devices are supported:
i2c:
bh1750 - light sensor (required)
bmp280 - temp/pressure sensor (and in bmXX80 range should work)
mpl3115a2 - temp/pressure sensor
ina2xx-adc - HWMON INA200 voltage/current sensor (required)

1wire:
w1-therm - ds18b20 temperature sensor

hwmod:
ina2xxx - voltage sensor

Additional sensors can be added by extending the LightSensor.py and TemperatureSensor.py classes.

Also, you must update /etc/modules file as follows:

```bash
i2c-dev
#bmp280
#bmp280-i2c
#mpl3115
bh1750
w1-therm
ina2xx-adc
```

The drivers required for each sensor must be specified here to make sure they are loaded at boot time.

## Services

First, the busdrivers script must be coped to /usr/bin. This script causes the loaded sensor to be allocated on the i2c bus.

To get the trailcam to start up, two services must be installed:

busdrivers.service
trailcam.service

Copy the above files to /etc/systemd/system.

Then run:

```bash
sudo systemctl enable busdrivers
sudo systemctl enable trailcam
```

## Config

The standard location for the config file is in /etc/trailcam. Copy the config-sample.yml to /etc/trailcam/config.yml and edit it accordingly.

BE CAREFUL: The voltage sensor, if enabled, can cause the system to halt on low power conditions. However, if you are running the system from a AC adapter lower then the battery voltage, the system will start, and then suddenly halt. It is important to only enable the low voltage shutdown once the system is in the field; otherwise, it may be required to pull the SD card from the RPi, and edit the trailcam config offline to stop the unwanted shutdowns.
