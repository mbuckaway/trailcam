import yaml
import logging
from webcamlib.Exceptions import ConfigError

config_logger = logging.getLogger('config')

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
            self.property_rotation = object['rotation']
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
    
    @property
    def rotation(self):
        return self.property_rotation

class ConfigSensors:
    """ Sensor section configuration """

    def __init__(self, object):
        try:
            self.property_temperature = ConfigTemperature(object['temperature'])
            self.property_light = ConfigLightSensor(object['light'])
            self.property_voltage = ConfigVoltageSensor(object['voltage'])
        except KeyError as e:
            raise ConfigError("Sensors Section: " + str(e.args))

    @property
    def temperature(self):
        return self.property_temperature

    @property
    def light(self):
        return self.property_light

    @property
    def voltage(self):
        return self.property_voltage


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
        """ Sensor types are mp3115a2 or BMP280 or ds18b20"""
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

class ConfigVoltageSensor:
    """ Voltage/Current Sensor section configuration """

    def __init__(self, object):
        try:
            self.property_enabled = object['enabled']
            self.property_type = object['type']
            self.property_address = object['address']
            # Rounding is optional. -1 means no rounding
            try:
                self.property_rounding = int(object['rounding'])
            except KeyError:
                self.property_rounding = -1
        except KeyError as e:
            raise ConfigError("Voltage Sensor Section: " + str(e.args))

    @property
    def sensortype(self):
        """ Sensor types are INA219 only at this point """
        return self.property_type.upper()

    @property
    def enabled(self):
        return self.property_enabled

    @property
    def address(self):
        return self.property_address

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
            self.property_tmpfilename = object['tmpfilename']
            self.property_archive = bool(object['archive'])
            self.property_extension = object['extension']
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

    @property
    def extension(self):
        return self.property_extension

    @property
    def tmpfilename(self):
        return self.property_tmpfilename

    @property
    def archive(self):
        return self.property_archive

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

class ConfigLED:
    """ LED config section """
    def __init__(self, object):
        try:
            self.property_enabled = object['enabled']
            self.property_gpiopin = int(object['gpiopin'])
        except KeyError as e:
            raise ConfigError('LED Section: ' + str(e.args))

    @property
    def enabled(self):
        return self.property_enabled

    @property
    def gpiopin(self):
        return self.property_gpiopin


class ConfigFTP:
    """ FTP config section """
    def __init__(self, object, enabled):
        try:
            self.property_enabled = object['enabled']
            if (enabled == False):
                config_logger.warning("FTP Disabled!")
                self.property_enabled = False
            self.property_server = object['server']
            self.property_user = object['user']
            self.property_password = object['password']
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
    def archive_dir(self):
        return self.property_archivedir

class ConfigTwitter:
    """ Twitter config section """
    def __init__(self, object, enabled):
        try:
            self.property_enabled = object['enabled']
            if (enabled == False):
                config_logger.warning("Twitter Disabled!")
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

class ConfigHWMon:
    """ HWMon config section """
    def __init__(self, object):
        try:
            self.property_shutdown_enabled = object['shutdown_enabled']
            twilio_section = object['twilio']
            self.property_twilio_enabled = twilio_section['enabled']
            self.property_twilio_account_sid = twilio_section['account_sid']
            self.property_twilio_auth_token = twilio_section['auth_token']
            self.property_twilio_phone_number = twilio_section['phone_number']

            message_section = object['message']
            self.property_message_warning = message_section['warning']
            self.property_message_shutdown = message_section['shutdown']

            self.property_smslimit = object['smslimit']

            # Don't bother with the phone numbers if SMS is disabled
            if (self.property_twilio_enabled):
                self.property_phone_numbers = object['phone_numbers']

            minvoltage_section = object['min_voltage']
            self.property_warning_voltage = minvoltage_section['warning']
            self.property_shutdown_voltage = minvoltage_section['shutdown']
            self.property_timefile = object['timefile']
        except KeyError as e:
            raise ConfigError('HWMon Section: ' + str(e.args))

    @property
    def shutdown_enabled(self):
        return self.property_shutdown_enabled
        
    @property
    def twilio_enabled(self):
        return self.property_twilio_enabled

    @property
    def twilio_account_sid(self):
        return self.property_twilio_account_sid

    @property
    def twilio_auth_token(self):
        return self.property_twilio_auth_token

    @property
    def twilio_phone_number(self):
        return self.property_twilio_phone_number

    @property
    def message_warning(self):
        return self.property_message_warning

    @property
    def message_shutdown(self):
        return self.property_message_shutdown

    @property
    def smslimit(self):
        return self.property_smslimit

    @property
    def phone_numbers(self):
        return self.property_phone_numbers

    @property
    def warning_voltage(self):
        return self.property_warning_voltage

    @property
    def shutdown_voltage(self):
        return self.property_shutdown_voltage

    @property
    def timefile(self):
        return self.property_timefile

class ConfigThingSpeak:
    """ ThinkSpeak config section """
    def __init__(self, object):
        try:
            self.property_enabled = object['enabled']
            self.property_writekey = object['writekey']
            self.property_channelid = object['channelid']
            self.property_timeout = object['timeout']
        except KeyError as e:
            raise ConfigError('ThinkSpeak Section: ' + str(e.args))

    @property
    def enabled(self):
        return self.property_enabled

    @property
    def writekey(self):
        return self.property_writekey

    @property
    def channelid(self):
        return self.property_channelid

    @property
    def timeout(self):
        return self.property_timeout

class ConfigProcess:
    """ Scheduler Process item section """
    def __init__(self, object):
        try:
            self.property_enabled = object['enabled']
            self.property_description = object['description']
            self.property_count = int(object['count'])
            self.property_functions = object['functions']
        except KeyError as e:
            raise ConfigError('Scheduler Process Section: ' + str(e.args))

    @property
    def enabled(self):
        return self.property_enabled

    @property
    def description(self):
        return self.property_description

    @property
    def count(self):
        return self.property_count

    @property
    def functions(self):
        return self.property_functions

class ConfigScheduler:
    """ Scheduler config section """
    def __init__(self, object):
        try:
            self.property_interval = int(object['interval'])
            self.property_processes = []
            for process in object['processes']:
                self.property_processes.append(ConfigProcess(process))
        except KeyError as e:
            raise ConfigError('Scheduler Section: ' + str(e.args[0]))

    @property
    def interval(self):
        return self.property_interval

    @property
    def processes(self):
        return self.property_processes

class ConfigRestAPI:
    """ RestAPI config section """
    def __init__(self, object):
        try:
            self.property_enabled = object['enabled']
            self.property_camera_id = int(object['camera_id'])
            self.property_host = object['host']
            self.property_api_key = object['api_key']
        except KeyError as e:
            raise ConfigError('RestAPI Section: ' + str(e.args[0]))

    @property
    def enabled(self):
        return self.property_enabled

    @property
    def camera_id(self):
        return self.property_camera_id

    @property
    def host(self):
        return self.property_host

    @property
    def api_key(self):
        return self.property_api_key

class ConfigTrailRestAPI:
    """ Trail RestAPI config section """
    def __init__(self, object):
        try:
            self.property_enabled = object['enabled']
            self.property_host = object['host']
        except KeyError as e:
            raise ConfigError('RestAPI Section: ' + str(e.args[0]))

    @property
    def enabled(self):
        return self.property_enabled

    @property
    def host(self):
        return self.property_host

class Config:
    """
    A class to deal with loading and parsing the config file and all the options within
    """

    def __init__(self, filename, ftpenabled = False, twitterenabled = False):
        self.filename = filename
        with open(filename) as config_data:
            self.config = yaml.full_load(config_data)
        # Load the sections of the config
        try:
            self.property_camera = ConfigCamera(self.config['camera'])
            self.property_sensors = ConfigSensors(self.config['sensors'])
            self.property_image = ConfigImage(self.config['image'])
            self.property_ftp = ConfigFTP(self.config['ftp'], ftpenabled)
            self.property_twitter = ConfigTwitter(self.config['twitter'], twitterenabled)
            self.property_annotate = ConfigAnnotate(self.config['annotate'])
            self.property_ledgreen = ConfigLED(self.config['ledgreen'])
            self.property_ledred = ConfigLED(self.config['ledred'])
            self.property_hwmon = ConfigHWMon(self.config['hwmon'])
            self.property_thingspeak = ConfigThingSpeak(self.config['thingspeak'])
            self.property_scheduler = ConfigScheduler(self.config['scheduler'])
            self.property_restapi = ConfigRestAPI(self.config['restapi'])
            self.property_trailapi = ConfigTrailRestAPI(self.config['trailapi'])
            config_logger.debug("Camera device: " + self.property_camera.device)
            config_logger.debug("Image size: " + str(self.property_image.width) + "x" + str(self.property_image.height))
            config_logger.debug("Image file: " + self.property_image.filename)
            config_logger.debug("Ftp Server: " + self.property_ftp.server)
            config_logger.debug("Ftp User: " + self.property_ftp.user)

        except KeyError as e:
            config_logger.exception("Invalid or missing key in section config: %s", e)
            raise e
        except ConfigError as e:
            config_logger.exception("Invalid or missing key in config: %s", e)
            raise e

    def dispose(self):
        pass

    @property
    def configfile(self):
        return self.filename

    @property
    def camera(self):
        return self.property_camera

    @property
    def sensors(self):
        return self.property_sensors

    @property
    def image(self):
        return self.property_image

    @property
    def annotate(self):
        return self.property_annotate

    @property
    def ledred(self):
        return self.property_ledred

    @property
    def ledgreen(self):
        return self.property_ledgreen

    @property
    def ftp(self):
        return self.property_ftp

    @property
    def twitter(self):
        return self.property_twitter

    @property
    def hwmon(self):
        return self.property_hwmon

    @property
    def thingspeak(self):
        return self.property_thingspeak

    @property
    def scheduler(self):
        return self.property_scheduler

    @property
    def restapi(self):
        return self.property_restapi

    @property
    def trailapi(self):
        return self.property_trailapi
