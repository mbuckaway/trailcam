import logging
from twython import Twython

class TwitterPost:
    """ 
    TwitterPost uploads the webcam image to twitter
    """
    def __init__(self, config, data):
        self.config = config
        self.data = data

    def post(self):
        if (self.config.twitter.enabled):
            logging.info("Posting to twitter...")
            try:
                api = Twython(self.config.twitter.consumerkey, self.config.twitter.consumersecret, self.config.twitter.accesskey, self.config.twitter.accesssecret) 
                logging.debug("Opening " + self.config.image.filename)
                photo = open(self.config.image.filename,'rb')
                response = api.upload_media(media=photo)
                logging.debug("Posting file and text...")
                api.update_status(status=self.data.annotation_twitter, media_ids=[response['media_id']])
                photo.close()                                    # close file and FTP
            except Exception as e:
                logging.error('Failed to Tweet the status: ' + str(e.args))
        else:
            logging.warn("Twitter disabled")
