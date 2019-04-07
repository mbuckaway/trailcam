import logging
import json
from datetime import datetime
import io

class TimeFile:
    """ Class to open a json data file and update the info """
    def __init__(self, hwmonconfig):
        self.hwmonconfig = hwmonconfig
        now = datetime.now()
        self.lastrundatetime = now
        self.lastsmsdatetime = now
        self.timefiledata = {}
    
    def _serialize(self, obj):
        if isinstance(obj, datetime):
            return { '_timestamp': obj.timestamp() }
        return super().default(obj)

    def _deserialize(self, obj):
        _isoformat = obj.get('_timestamp')
        if _isoformat is not None:
            return datetime.fromtimestamp(_isoformat)
        return obj

    def ReadData(self):
        with open(self.hwmonconfig.timefile) as json_data:
            self.timefiledata = json.load(json_data, object_hook=self._deserialize)
        self.lastrundatetime = self.timefiledata['lastrundatetime']
        self.lastruntime = self.timefiledata['lastsmsdatetime']

    def UpdateData(self):
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
                            separators=(',', ': '),
                            ensure_ascii=False,
                            default=self._serialize)
            outfile.write(to_unicode(str_))

    @property
    def LastRunDateTime(self):
        return self.lastrundatetime        

    @property
    def LastSmsSendDataTime(self):
        return self.lastsmsdatetime

