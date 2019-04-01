import logging
from twython import Twython

class TwitterPost:
    """ 
    TwitterPost uploads the webcam image to twitter
    """
    def __init__(self, filename, twitterconfig, annotation):
        self.property_filename = filename
        self.property_twitterconfig = twitterconfig
        self.property_annotation = annotation


    def post(self):
        if (self.property_twitterconfig.enabled):
            logging.info("Posting to twitter...")
            try:
                api = Twython(self.property_twitterconfig.consumerkey, self.property_twitterconfig.consumersecret, self.property_twitterconfig.accesskey, self.property_twitterconfig.accesssecret) 
                logging.debug("Opening " + self.property_filename)
                photo = open(self.property_filename,'rb')
                response = api.upload_media(media=photo)
                logging.debug("Posting file and text...")
                api.update_status(status=self.property_annotation, media_ids=[response['media_id']])
                photo.close()                                    # close file and FTP
            except Exception as e:
                logging.error('Failed to Tweet the status: ' + str(e.args))
        else:
            logging.warn("Twitter disabled")

if __name__ == '__main__':
  import doctest
  doctest.testmod()
