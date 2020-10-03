import ujson as json
from urllib import urequest
import logging

class FileRestClient:
    """ 
    Rest client to notify the database server of a new file to upload
    """
    def __init__(self, config):
        self.logger = logging.getLogger('restapiclient')
        self.config = config

    def _encodedata(self, postdata):
        data = json.dumps(postdata)
        data = str(data)
        data = data.encode('utf-8')
        return data

    def new_file(self, filename, directory, data):
        postdata = {
            "camera_id": self.config.restapi.camera_id,
            "filename": filename,
            "directory": directory,
            "data": data,
            "api_key": self.config.restapi.api_key
        }
        data = self._encodedata(postdata)

        req =  urequest.Request(self.config.restapi.host + '/api/photos/create.php', data=data)
        req.add_header('Content-Type', 'application/json')

        result = { "success": False }
        try:
            with urequest.urlopen(req) as response:
                datareturned = response.read().decode('utf-8')
            result = json.loads(datareturned)
            self.logger.info("Added new file to website {}/{}".format(directory, filename))
        except ValueError as e:
            self.logger.exception("Value error: %s", e)
        except OSError as e:    
            self.logger.exception("Http error: %s", e)
        except json.decoder.JSONDecodeError as e:
            self.logger.exception("JSON error: %s", e)
        return result

    def filelist(self):
        postdata = {
            "camera_id": self.config.restapi.camera_id,
            "count": 8,
            "api_key": self.config.restapi.api_key
        }
        data = self._encodedata(postdata)

        req =  urequest.Request(self.config.restapi.host + '/api/photos/last.php', data=data)
        req.add_header('Content-Type', 'application/json')

        result = { "success": False }
        try:
            with urequest.urlopen(req) as response:
                datareturned = response.read().decode('utf-8')
            result = json.loads(datareturned)
        except ValueError as e:
            self.logger.exception("Value error: %s", e)
        except OSError as e:    
            self.logger.exception("Http error: %s", e)
        except json.decoder.JSONDecodeError as e:
            self.logger.exception("JSON error: %s", e)
        return result

    def delete_by_name(self, filename, directory):
        postdata = {
            "filename": filename,
            "directory": directory,
            "api_key": self.config.restapi.api_key
        }
        data = self._encodedata(postdata)

        req =  urequest.Request(self.config.restapi.host + '/api/photos/deletebyname.php', data=data)
        req.add_header('Content-Type', 'application/json')

        result = { "success": False }
        try:
            with urequest.urlopen(req) as response:
                datareturned = response.read().decode('utf-8')
            result = json.loads(datareturned)
        except ValueError as e:
            self.logger.exception("Value error: %s", e)
        except OSError as e:    
            self.logger.exception("Http error: %s", e)
        except json.decoder.JSONDecodeError as e:
            self.logger.exception("JSON error: %s", e)
        return result
