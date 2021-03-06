import logging
import thingspeak
from webcamlib.Config import ConfigThingSpeak

class ThingSpeakData:
    """ Class to store data into a excel file for upload """
    def __init__(self, config, data):
        self.logging = logging.getLogger("thingspeak")
        self.config = config
        self.data = data
        self.thingspeak = thingspeak.Channel(self.config.thingspeak.channelid, api_key=self.config.thingspeak.writekey, timeout=self.config.thingspeak.timeout)

    def WriteData(self):
        status = "OK"
        self.logging.debug("Error is [{}]".format(self.data.lasterror))
        if (self.data.haserror):
            status = self.data.lasterror
        data = {}
        data['channel_id'] = self.config.thingspeak.channelid
        data['field1'] = self.data.voltage
        data['field2'] = self.data.current
        data['field3'] = self.data.temperature
        data['field4'] = self.data.light
        data['field5'] = self.data.pressure
        data['status'] = status
        self.thingspeak.update(data)
        self.data.clearerror()



