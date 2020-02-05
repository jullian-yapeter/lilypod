from spectrometer.noircam import NoirCam


class Spectrometer:

    def __init__(self, camera):
        self.camera = NoirCam()