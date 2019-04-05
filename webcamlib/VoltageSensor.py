from webcamlib.Config import Config, ConfigTemperature
import logging
from pathlib import PosixPath
from abc import ABC, abstractproperty
import board
import busio
import adafruit_ina219
from webcamlib.Exceptions import DeviceError, ConfigError

class AbstractVoltageSensor(ABC):
    """ Base class for the Voltage/Current sensor """
    def __init__(self, voltagesensor_config):
        self.property_sensor_config = voltagesensor_config

    @abstractproperty
    def voltage(self):
        pass

    @abstractproperty
    def current(self):
        pass

    @abstractproperty
    def bus(self):
        pass        


class INA219Sensor(AbstractVoltageSensor):
    """
    Class to read the sensor INA209 on the I2C bus

    To find the sensor id, make sure the i2c bus is enabled, the device is connected, and 
    INA209 module is loaded, and use the i2cdetect command. By default, the INA209 is on address 0x40
    and the linux module for it puts it in the hwmon directory which doesn't unfortunately expose
    the value. So, we end up using the Adafruit library for it. It would be better if we can just read some
    file to get the data instead of hammering the i2c bus, but I couldn't find it.

    """
    def __init__(self, voltagesensor_config):
        super().__init__(voltagesensor_config)
        self.property_bus = "i2c"
        self.i2cbus = busio.I2C(board.SCL, board.SDA)
        self.ina219 = adafruit_ina219.INA219(self.i2cbus)
        self.voltage_value = 0
        self.current_value = 0

    @property
    def voltage(self):
        return self.ina219.bus_voltage

    @property
    def current(self):
        return self.ina219.current


    @property
    def bus(self):
        return self.property_bus


class VoltageSensor:
    """ Main Class to read a Light sensor. Currently, the supported sensors are:
        INA209 - Volage/Current
        ..additional chips may be added in the future
    """

    def __init__(self, voltagesensor_config):
        try:
            if (voltagesensor_config.sensortype.upper() == "BH1750"):
                self.sensor = INA219Sensor(voltagesensor_config)
            else:
                raise ConfigError("Invalid voltage level sensor type: " + voltagesensor_config.sensortype)
        except DeviceError as e:
            logging.error("Unable to find sensor: " + str(e.args))
            raise e

    @property
    def voltage(self):
        return self.sensor.voltage

    @property
    def current(self):
        return self.sensor.current

    @property
    def bus(self):
        return self.sensor.bus

if __name__ == '__main__':
    import doctest
    doctest.testmod()
