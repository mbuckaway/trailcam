from webcamlib.Config import Config, ConfigTemperature
import logging
from pathlib import PosixPath
from abc import ABC, abstractproperty
from webcamlib.Exceptions import DeviceError, ConfigError

class AbstractTemperatureSensor(ABC):
    """ Base class for the temperature sensor """
    def __init__(self, temperature_config):
        self.property_sensor_config = temperature_config

    @abstractproperty
    def temperature(self):
        pass

    @abstractproperty
    def pressure(self):
        pass        

    @abstractproperty
    def bus(self):
        pass        

class NullSensor(AbstractTemperatureSensor):
    def __init__(self, temperature_config):
        super().__init__(temperature_config)
        self.property_bus = "null"

    @property
    def temperature(self):
        return 0

    @property
    def pressure(self):
        return 0

    @property
    def bus(self):
        return self.property_bus

class BMP280Sensor(AbstractTemperatureSensor):
    """
     Class to read the sensor BMP280 on the I2C bus

    To find the sensor id, make sure the i2c bus is enabled, the device is connected, and 
    mp3115a2 module is loaded. Additionally, you have to tell the i2c bus to read the chip
    with the 
    
    "echo bmp280 0x76" > /sys/bus/i2c/devices/i2c-1/new_device

    ...command. The i2c-1 bus number may change if the system has more than one i2c bus loadded.

     Then look in /sys/bus/i2c/devices directory for the 1-0076 directory.

     The 0x76 above and the 1-0076 represents the i2c bus id. The bus id can be determined
     with the i2cdetect command is needed. Some bmp280 sensors have ids of 0x77.

     The bme280 should also be supported but the humidity value will not be read

     """
    def __init__(self, temperature_config):
        super().__init__(temperature_config)
        self.property_bus = "i2c"
        devicepath = PosixPath("/sys/bus/i2c/devices").joinpath(temperature_config.device).joinpath("iio:device0")
        self.temperature_path = PosixPath(devicepath.joinpath("in_temp_input"))
        self.pressure_path = PosixPath(devicepath.joinpath("in_pressure_input"))
        # Make sure they exist
        if (not self.temperature_path.exists() and not self.temperature_path.is_file()):
            raise DeviceError(self.temperature_path)
        if (not self.pressure_path.exists() and not self.pressure_path.is_file()):
            raise DeviceError(self.pressure_path)

    @property
    def temperature(self):
        with self.temperature_path.open() as f:
            data = f.readline()
            data = str.strip(data)
        result = int(data)/1000
        if (self.property_sensor_config.rounding != -1):
            result = round(result, self.property_sensor_config.rounding)
        return (result)

    @property
    def pressure(self):
        with self.pressure_path.open() as f:
            data = f.readline()
            data = str.strip(data)
        result = float(data) * 10
        if (self.property_sensor_config.rounding != -1):
            result = round(result, self.property_sensor_config.rounding)
        return result

    @property
    def bus(self):
        return self.property_bus

class MP3115Sensor(AbstractTemperatureSensor):
    """
    Class to read the sensor MP3115 on the I2C bus

    To find the sensor id, make sure the i2c bus is enabled, the device is connected, and 
    mp3115a2 module is loaded. Additionally, you have to tell the i2c bus to read the chip
    with the 
    
    "echo mp3115a2 0x60" > /sys/bus/i2c/devices/i2c-1/new_device

    ...command. The i2c-1 bus number may change if the system has more than one i2c bus loadded.

     Then look in /sys/bus/i2c/devices directory for the 1-0060 directory.

     The 0x60 above and the 1-0060 represents the i2c bus id. The bus id can be determined
     with the i2cdetect command is needed.

    """
    def __init__(self, temperature_config):
        super().__init__(temperature_config)
        self.property_bus = "i2c"
        devicepath = PosixPath("/sys/bus/i2c/devices").joinpath(temperature_config.device).joinpath("iio:device0")
        self.temperature_path_raw = PosixPath(devicepath.joinpath("in_temp_raw"))
        self.temperature_path_scale = PosixPath(devicepath.joinpath("in_temp_scale"))
        self.pressure_path_raw = PosixPath(devicepath.joinpath("in_pressure_raw"))
        self.pressure_path_scale = PosixPath(devicepath.joinpath("in_pressure_scale"))
        # Make sure they exist
        if (not self.temperature_path_raw.exists() and not self.temperature_path_raw.is_file()):
            raise DeviceError(self.temperature_path_raw)
        if (not self.temperature_path_scale.exists() and not self.temperature_path_scale.is_file()):
            raise DeviceError(self.temperature_path_scale)
        if (not self.pressure_path_raw.exists() and not self.pressure_path_raw.is_file()):
            raise DeviceError(self.pressure_path_raw)
        if (not self.pressure_path_scale.exists() and not self.pressure_path_scale.is_file()):
            raise DeviceError(self.pressure_path_scale)

    @property
    def temperature(self):
        with self.temperature_path_raw.open() as f:
            data_raw = f.readline()
        with self.temperature_path_scale.open() as f:
            data_scale = f.readline()
        result = int(data_raw)*float(data_scale)
        if (self.property_sensor_config.rounding != -1):
            result = round(result, self.property_sensor_config.rounding)
        return result

    @property
    def pressure(self):
        with self.pressure_path_raw.open() as f:
            data_raw = f.readline()
        with self.pressure_path_scale.open() as f:
            data_scale = f.readline()
        result = int(data_raw) * float(data_scale) * 10
        if (self.property_sensor_config.rounding != -1):
            result = round(result, self.property_sensor_config.rounding)
        return result

    @property
    def bus(self):
        return self.property_bus

class DS18B20Sensor(AbstractTemperatureSensor):
    """
    Class to read the sensor DS18B20 on the one wire bus

    To find the sensor id, make sure the one wire bus is enabled, the device is connected, and 
    w1_therm module is loaded. Then look in /sys/bus/w1/devices for a file startig with 28-*. 
    Record that number and that is the device. The device will be different for each sensor
    on the w1 bus.

    """

    def __init__(self, temperature_config):
        super().__init__(temperature_config)
        self.property_bus = "w1"
        devicepath = PosixPath("/sys/bus/w1/devices").joinpath(temperature_config.device)
        self.temperature_path = PosixPath(devicepath.joinpath("w1_slave"))
        # Make sure they exist
        if (not self.temperature_path.exists() and not self.temperature_path.is_file()):
            raise DeviceError(self.temperature_path)

    @property
    def temperature(self):
        with self.temperature_path.open() as f:
            f.readline()
            line = f.readline()

        data = line.split('=')
        result = int(data[1])/1000
        if (self.property_sensor_config.rounding != -1):
            result = round(result, self.property_sensor_config.rounding)
        return result

    @property
    def pressure(self):
        return 0

    @property
    def bus(self):
        return self.property_bus

class TemperatureSensor:
    """ Main Class to read a temperature sensor. Currently, the supported sensors are:
        DS18B20 - temperature only
        BMP280 - temperature and pressure
        MP3115A2 - temperature and pressure

        Reading pressure from a sensor that does not support it will return 0
    """
    def __init__(self, temperature_config):
        try:
            self.sensor = NullSensor(temperature_config)
            logging.debug("Found temperature sensor: " + temperature_config.sensortype.upper())
            if (temperature_config.sensortype.upper() == "DS18B20"):
                self.sensor = DS18B20Sensor(temperature_config)
            elif (temperature_config.sensortype.upper() == "MP3115A2"):
                self.sensor = MP3115Sensor(temperature_config)
            elif (temperature_config.sensortype.upper() == "BMP280"):
                self.sensor = BMP280Sensor(temperature_config)
            else:
                raise ConfigError("Invalid temperature sensor type: " + temperature_config.sensortype)
        except DeviceError as e:
            logging.error("Unable to find sensor: " + str(e.args))
            raise e

    @property
    def temperature(self):
        return self.sensor.temperature

    @property
    def pressure(self):
        return self.sensor.pressure

    @property
    def bus(self):
        return self.sensor.bus


if __name__ == '__main__':
  import doctest
  doctest.testmod()
