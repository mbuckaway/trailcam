import json
from urllib import request, parse, error
import ssl
import logging

class TrailRestClient:
    """ 
    Rest client to get the hydrocut status
    """
    def __init__(self, config):
        self.logger = logging.getLogger('trailapiclient')
        self.config = config

    def status(self):
        req =  request.Request(self.config.trailapi.host, unverifiable=True)

        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with request.urlopen(req, context=ctx) as response:
                datareturned = response.read().decode('utf-8')
            statusreturned = json.loads(datareturned)
        except error.HTTPError as e:
            self.logger.exception("Http error: %s", e)
        except error.URLError as e:    
            self.logger.exception("Http error: %s", e)
        except json.decoder.JSONDecodeError as e:
            self.logger.exception("JSON error: %s", e)
        isopen = True
        if statusreturned and 'status' in statusreturned and statusreturned['status'] == 'closed':
            isopen = False
        return isopen
