from webcamlib.Config import Config
import v4l2capture
from PIL import Image
from picamera import PiCamera
import logging
import ephem
import datetime
import math
from gpiozero import LED
from pathlib import PosixPath
import select
import time

class Camera:
    """
    Class to represent the supported cameras, flash the led if enabled, and take a photo
    >>> from logging_configurator import configure_logging
    >>> configure_logging()
    >>> configFile = Config('config-sample.json')
    >>> camera = Camera(configFile.camera, configFile.image, configFile.led, 0)
    >>> camera.SnapPhoto()
    >>> print("done")
    done
    """
    def __init__(self, config_camera, config_image, config_led, lightvalue):
        self.config_camera = config_camera
        self.config_image = config_image
        self.config_led = config_led
        self.lightvalue = lightvalue
        self.led = LED(self.config_led.gpiopin)

    def SnapPhoto(self):
        if (self.config_camera.cameratype.upper() == 'PI'):
            logging.debug("Using PI camera")
            self.snapshotPiCamera()
        else:    
            logging.debug("Using USB camera")
            self.snapshotv4l()


    def blinkled(self):
        if (self.config_led.enabled):
            logging.debug("Flashing Indicator Led")
            self.led.blink(self.config_led.slowtime, self.config_led.slowtime, self.config_led.slowcount, False)
            self.led.blink(self.config_led.fasttime, self.config_led.fasttime, self.config_led.fastcount, False)
            self.led.on()

    def ledoff(self):
        if (self.config_led.enabled):
            logging.debug("Indicator Led off")
            self.led.off()

    def isdaytime(self):
        sun = ephem.Sun()
        observer = ephem.Observer()
        #  Define your coordinates here
        observer.lat, observer.lon, observer.elevation = self.config_camera.latitude, self.config_camera.logitude, self.config_camera.elevation
        # Set the time (UTC) here
        observer.date = datetime.datetime.utcnow()
        sun.compute(observer)
        current_sun_alt = sun.alt*180/math.pi
        result = True
        # If the sun is -6 or greater, we are nightime
        if (current_sun_alt<-6):
            result = False
        logging.info("System is in day mode: " + str(result))
        return result

    def snapshotPiCamera(self):
        try:
            with PiCamera() as camera:
                camera.resolution = (self.config_image.width, self.config_image.height)
                camera.awb_mode = 'auto'
                camera.rotation = self.config_camera.rotation
                # Get the time and see if we should be using night mode
                if (self.lightvalue == 0):
                    if (self.isdaytime):
                        #camera.exposure_mode = 'beach'
                        camera.iso = 100
                    else:
                        camera.exposure_mode = 'nightpreview'
                        camera.iso = 1200
                        camera.brightness = 60
                else:            
                    if self.lightvalue>200:
                        camera.iso = 100
                    else:
                        camera.exposure_mode = 'nightpreview'
                        camera.iso = 1200
                        camera.brightness = 60
                    path = PosixPath(self.config_image.filename)
                    # Assume jpg
                    imagetype = "jpeg"
                    if path.suffix.upper() == "PNG":
                        imagetype = "png"
                    self.blinkled()
                    camera.capture(self.config_image.filename, format=imagetype, use_video_port=False)
        except Exception as e:
            logging.error("Camera was unable to capture an image: " + str(e.args))
        finally:
            self.ledoff()

    def snapshotv4l(self):
        logging.info("Taking photo from device: " + self.config_camera.device)
        try:
            video = v4l2capture.Video_device(self.config_camera.device)
            size_x, size_y = video.set_format(self.config_image.width, self.config_image.height)
            video.create_buffers(1)
            video.start()
            if (self.config_camera.delay>0):
                time.sleep(self.config_camera.delay)
            self.blinkled()
            video.queue_all_buffers()
            select.select((video,), (), ())

            image_data = video.read()
            video.stop()
            video.close()
            image = Image.frombytes("RGB", (size_x, size_y), image_data)
            logging.info("Saving file: " + self.config_image.filename)
            image.save(self.config_image.filename)
        except Exception as e:
            logging.error("Error taking v4l image: " + str(e.args))
        finally:
            self.ledoff()

if __name__ == '__main__':
  import doctest
  doctest.testmod()

