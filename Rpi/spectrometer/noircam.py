from io import BytesIO
from time import sleep

from picamera import PiCamera
from PIL import Image


class NoirCam:

    def __init__(self):
        self.camera = PiCamera()
        self.resolution = (1024, 768)
        self.photo = None

        self.camera.resolution = self.resolution

    def take_photo(self):
        stream = BytesIO()
        self.camera.start_preview()
        sleep(2)
        self.camera.capture(stream, format='jpeg')
        stream.seek(0)
        self.photo = Image.open(stream)
