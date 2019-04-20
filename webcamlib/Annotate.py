from webcamlib.Config import Config, ConfigTemperature, ConfigLightSensor
import logging
from pathlib import PosixPath
import datetime

class Annotate:
    def __init__(self, config, data):
        self.logger = logging.getLogger('annotate')
        self.annotate = config
        self.data = data

    def Annotate(self):
        self.logger.debug("Getting temperature...")
        date = datetime.datetime.now().strftime("%B %d, %Y %I:%M%p")
        # Let's substitude our vars
        line = self.annotate.format
        line = line.replace('%%DATE%%', date)
        line = line.replace('%%TEMP%%', str(self.data.temperature))
        line = line.replace('%%PRES%%', str(self.data.pressure))
        line = line.replace('%%LIGHT%%', str(self.data.light))
        self.data.annotation_photo = line
        self.logger.debug("Annotation (photo): " + line)

        line = self.annotate.format_twitter
        line = line.replace('%%DATE%%', date)
        line = line.replace('%%TEMP%%', str(self.data.temperature))
        line = line.replace('%%PRES%%', str(self.data.pressure))
        line = line.replace('%%LIGHT%%', str(self.data.light))
        self.data.annotation_twitter = line
        self.logger.debug("Annotation (photo): " + line)
