import logging
import json
import time
import datetime
import io

class TimeFile:
    """ Class to open a json data file and update the info """
    def __init__(self, hwmonconfig):
        self.hwmonconfig = hwmonconfig
        self.lastrundatetime = datetime.datetime()
        self.lastsmsdatetime = datetime.datetime()
    
    def ReadData(self):
        with open(self.hwmonconfig.timefile) as json_data:
            self.timefiledata = json.load(json_data)
        self.lastrundatetime = self.timefiledata['lastrundatetime']
        self.lastruntime = self.timefiledata['lastruntime']

    def UpdateDate(self):
        # Borrowed from https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
        try:
            to_unicode = unicode
        except NameError:
            to_unicode = str
        self.timefiledata['lastrundatetime'] = self.lastrundatetime
        self.timefiledata['lastsmsdatetime'] = self.lastruntime
        with io.open(self.hwmonconfig.timefile, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(self.timefiledata,
                            indent=4, sort_keys=True,
                            separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(str_))

    @property
    def LastRunDateTime(self):
        return self.lastrundatetime        

    @property
    def LastSmsSendDataTime(self):
        return self.lastsmsdatetime

