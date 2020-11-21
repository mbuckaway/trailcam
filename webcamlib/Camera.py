from webcamlib.Config import Config
#import v4l2capture
from PIL import Image, ImageFont, ImageDraw
from picamera import PiCamera
import logging
import ephem
import datetime
import math
import select
import os
import time

class Camera:
    """
    Class to represent the supported cameras, and take a photo
    done
    """
    def __init__(self, config, data):
        self.logger = logging.getLogger('camera')
        self.config = config
        self.data = data
        fontpath = config.annotate.font
        if not os.path.exists(fontpath):
            self.logger.error("Font path " + config.annotate.font + " does not exist. Annotation disabled")
            self.config.annotate.enabled = False

    def dispose(self):
        pass
        
    def SnapPhoto(self):
        if (self.config.camera.cameratype.upper() == 'PI'):
            self.logger.debug("Using PI camera")
            self.snapshotPiCamera()
        else:    
            self.logger.debug("Using USB camera")
            self.snapshotv4l()

    def isdaytime(self):
        sun = ephem.Sun()
        observer = ephem.Observer()
        #  Define your coordinates here
        observer.lat, observer.lon, observer.elevation = self.config.camera.latitude, self.config.camera.logitude, self.config.camera.elevation
        # Set the time (UTC) here
        observer.date = datetime.datetime.utcnow()
        sun.compute(observer)
        current_sun_alt = sun.alt*180/math.pi
        result = True
        # If the sun is -6 or greater, we are nightime
        if (current_sun_alt<-6):
            result = False
        self.logger.info("System is in day mode: " + str(result))
        return result

    def snapshotPiCamera(self):
        try:
            with PiCamera() as camera:
                self.logger.debug("Taking a picture with the PI camera")
                camera.resolution = (self.config.image.width, self.config.image.height)
                camera.awb_mode = 'auto'
                camera.rotation = self.config.camera.rotation
                # Get the time and see if we should be using night mode
                if (self.data.light == 0):
                    if (self.isdaytime):
                        camera.iso = 100
                    else:
                        camera.exposure_mode = 'nightpreview'
                        camera.iso = 1200
                        camera.brightness = 60
                else:            
                    if self.data.light>200:
                        camera.iso = 100
                    else:
                        camera.exposure_mode = 'nightpreview'
                        camera.iso = 1200
                        camera.brightness = 60
                # Assume jpg
                imagetype = "jpeg"
                if self.config.image.extension.upper() == "PNG":
                    imagetype = "png"
                filename = self.config.image.filename
                if self.config.image.archive:
                    now = datetime.datetime.now()
                    pathobj = os.path.join(self.config.image.directory, now.strftime("%Y%m/%d"))
                    if not os.path.exists(pathobj):
                        os.makedirs(pathobj)
                    fullfilename =  self.config.image.filename + "-" + now.strftime("%Y%m%d-%H%M%S") + "." + self.config.image.extension
                    filename = os.path.join(pathobj, fullfilename)
                    self.logger.info("Achiving image to: " + filename)
                camera.capture(filename, format=imagetype, use_video_port=False)
        except Exception as e:
            self.logger.error("Camera was unable to capture an image: " + str(e.args))

    def snapshotv4l(self):
        self.logger.info("Taking photo from device: " + self.config.camera.device)
        try:
            video = v4l2capture.Video_device(self.config.camera.device)
            size_x, size_y = video.set_format(self.config.image.width, self.config.image.height)
            video.create_buffers(1)
            video.start()
            if (self.config.camera.delay>0):
                time.sleep(self.config.camera.delay)
            self.blinkled()
            video.queue_all_buffers()
            select.select((video,), (), ())

            image_data = video.read()
            video.stop()
            video.close()
            image = Image.frombytes("RGB", (size_x, size_y), image_data)
            self.logger.info("Saving file: " + self.config.image.filename)
            image.save(self.config.image.filename)
        except Exception as e:
            self.logger.error("Error taking v4l image: " + str(e.args))

    def AnnotateImage(self):
        if (self.config.annotate.enabled == True):
            base = Image.open(self.config.image.filename).convert('RGBA')
            txt = Image.new('RGBA', base.size, (255,255,255,0))
            font = ImageFont.truetype(self.config.annotate.font, self.config.annotate.size)
            draw = ImageDraw.Draw(txt)
            # Assume bottom for now
            pos_x = base.height - 30
            draw.text((10, pos_x), self.data.annotation_photo, font=font,fill=(255,255,255,128))
            out = Image.alpha_composite(base, txt)

            self.logger.info("Saving image with weather data")
            out.convert('RGB').save(self.config.image.filename)
