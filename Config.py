import json
import logging
import distutils.util
from Exceptions import ConfigError

class ConfigCamera:
    """ Camera section configuration """

    def __init__(self, object):
        try:
            self.property_cameratype = object['type']
            self.property_device = object['device']
            self.property_delay = object['delay']
            self.property_latitude = object['latitude']
            self.property_longitude = object["longitude"]
            self.property_elevation = object["elevation"]
        except KeyError as e:
            raise ConfigError("Camera Section: " + str(e.args))

    @property
    def cameratype(self):
        return self.property_cameratype

    @property
    def device(self):
        return self.property_device

    @property
    def delay(self):
        return self.property_delay

    @property
    def latitude(self):
        return self.property_latitude

    @property
    def longitude(self):
        return self.property_longitude

    @property
    def elevation(self):
        return self.property_elevation

class ConfigTemperature:
    """ Sensor section configuration """

    def __init__(self, object):
        try:
            self.property_enabled = object['enabled']
            self.property_type = object['type']
            self.property_device = object['device']
            # Rounding is optional. -1 means no rounding
            try:
                self.property_rounding = int(object['rounding'])
            except KeyError:
                self.property_rounding = -1
        except KeyError as e:
            raise ConfigError("Sensor Section: " + str(e.args))

    @property
    def sensortype(self):
        """ Sensor types are mp3115a2 or BMP280 """
        return self.property_type.upper()

    @property
    def enabled(self):
        return self.property_enabled

    @property
    def device(self):
        return self.property_device

    @property
    def rounding(self):
        return self.property_rounding

class ConfigLightSensor:
    """ Light Sensor section configuration """

    def __init__(self, object):
        try:
            self.property_enabled = object['enabled']
            self.property_type = object['type']
            self.property_device = object['device']
            # Rounding is optional. -1 means no rounding
            try:
                self.property_rounding = int(object['rounding'])
            except KeyError:
                self.property_rounding = -1
        except KeyError as e:
            raise ConfigError("Light Sensor Section: " + str(e.args))

    @property
    def sensortype(self):
        """ Sensor types are bh1750 only at this point """
        return self.property_type.upper()

    @property
    def enabled(self):
        return self.property_enabled

    @property
    def device(self):
        return self.property_device

    @property
    def rounding(self):
        return self.property_rounding

class ConfigImage:
    """ Image config section """
    def __init__(self, object):
        try:
            self.property_width = object['width']
            self.property_height = object['height']
            self.property_filename = object['filename']
        except KeyError as e:
            raise ConfigError("Image Section: " + str(e.args))

    @property
    def width(self):
        return self.property_width

    @property
    def height(self):
        return self.property_height

    @property
    def filename(self):
        return self.property_filename

class ConfigAnnotate:
    """ Annotate config section """
    def __init__(self, object):
        try:
            self.property_enabled = object['enabled']
            self.property_font = object['font']
            self.property_format = object['format']
            self.property_format_twitter = object['format_twitter']
            self.property_size = int(object['size'])
            self.property_position = object['position']
        except KeyError as e:
            raise ConfigError("Annotate Section: " + str(e.args))

    @property
    def enabled(self):
        return self.property_enabled

    @property
    def font(self):
        return self.property_font

    @property
    def format(self):
        return self.property_format

    @property
    def format_twitter(self):
        return self.property_format_twitter

    @property
    def size(self):
        return self.property_size

    @property
    def position(self):
        return self.property_position

class ConfigFTP:
    """ FTP config section """
    def __init__(self, object, enabled):
        try:
            self.property_enabled = object['enabled']
            if (enabled == False):
                logging.warn("FTP Disabled!")
                self.property_enabled = False
            self.property_server = object['server']
            self.property_user = object['user']
            self.property_password = object['password']
            self.property_remotefile = object['remotefile']
            self.property_archivedir = object['archive_dir']
        except KeyError as e:
            raise ConfigError('FTP Section: ' + str(e.args))

    @property
    def enabled(self):
        return self.property_enabled

    @property
    def server(self):
        return self.property_server

    @property
    def user(self):
        return self.property_user

    @property
    def password(self):
        return self.property_password

    @property
    def remotefile(self):
        return self.property_remotefile

    @property
    def archive_dir(self):
        return self.property_archivedir

class ConfigTwitter:
    """ Twitter config section """
    def __init__(self, object, enabled):
        try:
            self.property_enabled = object['enabled']
            if (enabled == False):
                logging.warn("Twitter Disabled!")
                self.property_enabled = False
            self.property_consumerkey = object['ConsumerKey']
            self.property_consumersecret = object['ConsumerSecret']
            self.property_accesskey = object['AccessKey']
            self.property_accesssecret = object['AccessSecret']
        except KeyError as e:
            raise ConfigError('Twitter Section: ' + str(e.args))

    @property
    def enabled(self):
        return self.property_enabled

    @property
    def consumersecret(self):
        return self.property_consumersecret

    @property
    def consumerkey(self):
        return self.property_consumerkey

    @property
    def accesskey(self):
        return self.property_accesskey

    @property
    def accesssecret(self):
        return self.property_accesssecret

class Config:
    """ A class to deal with loading and parsing the config file and all the options within

    >>> args.ftp = True
    >>> args.twitter = True
    >>> configFile = Config('config-sample.json', args)
    >>> print(configFile.camera.cameratype)
    pi
    >>> print(configFile.camera.device)
    /dev/video0
    >>> print(configFile.camera.delay)
    2
    >>> print(configFile.camera.latitude)
    43.4873066
    >>> print(configFile.camera.longitude)
    -80.4841633
    >>> print(configFile.camera.elevation)
    400
    >>> print(configFile.temperature.enabled)
    True
    >>> print(configFile.lightsensor.enabled)
    True
    >>> print(configFile.image.width)
    1440
    >>> print(configFile.image.height)
    810
    >>> print(configFile.image.filename)
    /home/user/webcam.jpg
    >>> print(configFile.ftp.server)
    servername
    >>> print(configFile.twitter.consumersecret)
    CONSUMER SECRET
    """

    def __init__(self, filename, args):
        self.filename = filename
        with open(filename) as json_data:
            self.config = json.load(json_data)
        # Load the sections of the config
        try:
            self.property_camera = ConfigCamera(self.config['camera'])
            self.property_temperature = ConfigTemperature(self.config['temperature'])
            self.property_lightsensor = ConfigLightSensor(self.config['lightsensor'])
            self.property_image = ConfigImage(self.config['image'])
            self.property_ftp = ConfigFTP(self.config['ftp'], args.ftp)
            self.property_twitter = ConfigTwitter(self.config['twitter'], args.twitter)
            self.property_annotate = ConfigAnnotate(self.config['annotate'])
            logging.debug("Camera device: " + self.property_camera.device)
            logging.debug("Sensor Type: " + self.property_temperature.sensortype)
            logging.debug("Sensor Device: " + self.property_temperature.device)
            logging.debug("Image size: " + str(self.property_image.width) + "x" + str(self.property_image.height))
            logging.debug("Image file: " + self.property_image.filename)
            logging.debug("Ftp Server: " + self.property_ftp.server)
            logging.debug("Ftp User: " + self.property_ftp.user)

        except KeyError as e:
            logging.error("Invalid or missing key in section config: " + str(e.args))
        except ConfigError as e:
            logging.error("Invalid or missing key in config: " + e.section)


    @property
    def configfile(self):
        return self.filename

    @property
    def camera(self):
        return self.property_camera

    @property
    def temperature(self):
        return self.property_temperature

    @property
    def lightsensor(self):
        return self.property_lightsensor

    @property
    def image(self):
        return self.property_image

    @property
    def annotate(self):
        return self.property_annotate

    @property
    def ftp(self):
        return self.property_ftp

    @property
    def twitter(self):
        return self.property_twitter

if __name__ == '__main__':
  import doctest
  doctest.testmod()


