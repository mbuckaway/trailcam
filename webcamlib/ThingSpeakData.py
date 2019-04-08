import logging
import thingspeak
from webcamlib.Config import ConfigThingSpeak

class ThingSpeakData:
    """ Class to store data into a excel file for upload """
    def __init__(self, thinkspeakconfig):
        self.thinkspeakconfig = thinkspeakconfig
        self.thingspeak = thingspeak.Channel(self.thinkspeakconfig.channelid, api_key=self.thinkspeakconfig.writekey, timeout=self.thinkspeakconfig.timeout)

    def WriteData(self, voltage, current, temperature, lightlevel):
        data = {}
        data['channel_id'] = 738696
        data['field1'] = voltage
        data['field2'] = current
        data['field3'] = temperature
        data['field4'] = lightlevel
        data['status'] = "System OK"
        self.thingspeak.update(data)



