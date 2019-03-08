from Config import Config, ConfigTemperature, ConfigLightSensor
import logging
from pathlib import PosixPath
from PIL import Image, ImageFont, ImageDraw
import datetime
from TemperatureSensor import TemperatureSensor
from LightSensor import LightSensor

class Annotate:
    def __init__(self, config_annotate, config_image, config_temperature, config_lightsensor):
        self.config_annotate = config_annotate
        self.config_image = config_image
        self.config_temperature = config_temperature
        self.config_lightsensor = config_lightsensor
        fontpath = PosixPath(config_annotate.font)
        if (not fontpath.exists()):
            logging.error("Font path " + config_annotate.font + " does not exist. Annotation disabled")
            self.config_annotate.enabled = False

    def ReadSensors(self):
        logging.debug("Getting temperature...")
        temperaturesensor = TemperatureSensor(self.config_temperature)
        self.tempdata = temperaturesensor.temperature
        self.presdata = temperaturesensor.pressure
        logging.info("Temperature data: " + str(self.tempdata) + "C")
        logging.info("Pressure data: " + str(self.presdata) + "hPa")

        lightsensor = LightSensor(self.config_lightsensor)
        self.lightdata = lightsensor.lightlevel
        logging.info("Light data: " + str(self.lightdata) + "Lux")
        date = datetime.datetime.now().strftime("%B %d, %Y %I:%M%p")
        # Let's substitude our vars
        line = self.config_annotate.format
        line = line.replace('%%DATE%%', date)
        line = line.replace('%%TEMP%%', str(self.tempdata))
        line = line.replace('%%PRES%%', str(self.presdata))
        line = line.replace('%%LIGHT%%', str(self.lightdata))
        self.property_annotation = line
        logging.debug("Annotation: " + line)

        line = self.config_annotate.format_twitter
        line = line.replace('%%DATE%%', date)
        line = line.replace('%%TEMP%%', str(self.tempdata))
        line = line.replace('%%PRES%%', str(self.presdata))
        line = line.replace('%%LIGHT%%', str(self.lightdata))
        self.property_annotation_twitter = line


    def UpdateImage(self):
        if (self.config_annotate.enabled == True):
            base = Image.open(self.config_image.filename).convert('RGBA')
            txt = Image.new('RGBA', base.size, (255,255,255,0))
            font = ImageFont.truetype(self.config_annotate.font, self.config_annotate.size)
            draw = ImageDraw.Draw(txt)
            # Assume bottom for now
            pos_x = base.height - 30
            draw.text((10, pos_x), self.property_annotation, font=font,fill=(255,255,255,128))
            out = Image.alpha_composite(base, txt)

            logging.info("Saving image with weather data")
            out.convert('RGB').save(self.config_image.filename)

    @property
    def annotation(self):
        return self.property_annotation

    @property
    def annotation_twitter(self):
        return self.property_annotation_twitter

    @property
    def light_level(self):
        return self.lightdata
