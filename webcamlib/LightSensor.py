from webcamlib.Config import Config, ConfigTemperature
import logging
from pathlib import PosixPath
from abc import ABC, abstractproperty
from webcamlib.Exceptions import DeviceError, ConfigError

class AbstractLightSensor(ABC):
    """ Base class for the light sensor """
    def __init__(self, lightsensor_config):
        self.property_sensor_config = lightsensor_config

    @abstractproperty
    def lightlevel(self):
        pass

    @abstractproperty
    def bus(self):
        pass        

    def dispose(self):
        pass


class BH1750Sensor(AbstractLightSensor):
    """
    Class to read the sensor BH1750 on the I2C bus

    To find the sensor id, make sure the i2c bus is enabled, the device is connected, and 
    BH1750 module is loaded. Additionally, you have to tell the i2c bus to read the chip
    with the 
    
    "echo bh1750 0x23" > /sys/bus/i2c/devices/i2c-1/new_device

    ...command. The i2c-1 bus number may change if the system has more than one i2c bus loadded.

     Then look in /sys/bus/i2c/devices directory for the 1-0023 directory.

     The 0x23 above and the 1-0023 represents the i2c bus id. The bus id can be determined
     with the i2cdetect command is needed.

    """
    def __init__(self, lightsensor_config):
        super().__init__(lightsensor_config)
        self.property_bus = "i2c"
        devicepath = PosixPath("/sys/bus/i2c/devices").joinpath(lightsensor_config.device).joinpath("iio:device0")
        self.lightsensor_path_raw = PosixPath(devicepath.joinpath("in_illuminance_raw"))
        self.lightsensor_path_scale = PosixPath(devicepath.joinpath("in_illuminance_scale"))
        # Make sure they exist
        if (not self.lightsensor_path_raw.exists() and not self.lightsensor_path_raw.is_file()):
            raise DeviceError(self.lightsensor_path_raw)
        if (not self.lightsensor_path_scale.exists() and not self.lightsensor_path_scale.is_file()):
            raise DeviceError(self.lightsensor_path_scale)

    def dispose(self):
        pass

    @property
    def lightlevel(self):
        with self.lightsensor_path_raw.open() as f:
            data_raw = f.readline()
        with self.lightsensor_path_scale.open() as f:
            data_scale = f.readline()
        result = int(data_raw)*float(data_scale)
        if (self.property_sensor_config.rounding != -1):
            result = round(result, self.property_sensor_config.rounding)
        return result

    @property
    def bus(self):
        return self.property_bus


class LightSensor:
    """ Main Class to read a Light sensor. Currently, the supported sensors are:
        BH1750 - light level
        ..additional chips may be added in the future

        Reading pressure from a sensor that does not support it will return 0
    """
    def __init__(self, lightsensor_config):
        try:
            if (lightsensor_config.sensortype.upper() == "BH1750"):
                self.sensor = BH1750Sensor(lightsensor_config)
            else:
                raise ConfigError("Invalid light level sensor type: " + lightsensor_config.sensortype)
        except DeviceError as e:
            logging.error("Unable to find sensor: " + str(e.args))

    def dispose(self):
        self.sensor.dispose()

    @property
    def lightlevel(self):
        return self.sensor.lightlevel

    @property
    def bus(self):
        return self.sensor.bus

if __name__ == '__main__':
    import doctest
    doctest.testmod()
