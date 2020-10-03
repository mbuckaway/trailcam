import ujson as json
from urllib import urequest
import logging

class TrailStatusRestClient:
    """ 
    Rest client to notify the database server of a new file to upload
    """
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config

    def status(self):
        req =  urequest.Request(self.config.trailrestapi.host, data=none)
        req.add_header('Content-Type', 'application/json')

        result = { "success": False }
        try:
            with urequest.urlopen(req) as response:
                datareturned = response.read().decode('utf-8')
            statusinfo = json.loads(datareturned)
        except ValueError as e:
            self.logger.exception("Value error: %s", e)
        except OSError as e:    
            self.logger.exception("Http error: %s", e)
        except json.decoder.JSONDecodeError as e:
            self.logger.exception("JSON error: %s", e)
        isopen = true
        if 'status' in statusinfo and statusinfo['status'] == 'closed':
                isopen = false
        return isopen
