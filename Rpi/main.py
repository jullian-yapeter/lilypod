from cloudcomm.cloudcomm import LilypodFirestore, LilypodObject
from serialcomm.serialcomm import Serialcomm
from spectrometer import spectrometer

from logs.logs import logs


class LpodProc():
    def __init__(self, name):
        self.lilypod = LilypodObject(name=name, location=u'Waterloo', ph=0.0, conductivity=0.0,
                                     spectroscopy={'low': 0, 'high': 0})
        self.lilypodFirestore = LilypodFirestore(dbName=u'lilypods')
        self.serialcomm = Serialcomm(9600)

    def update_db(self, name=None, location=None, ph=None, conductivity=None, spectroscopy=None):
        if name is not None:
            self.lilypod.name = name
        if location is not None:
            self.lilypod.location = location
        if ph is not ph:
            self.lilypod.ph = ph
        if conductivity is not None:
            self.lilypod.conductivity = conductivity
        if spectroscopy is not None:
            self.lilypod.spectroscopy = spectroscopy
        if (self.lilypodFirestore.write_to_db(self.lilypod)):
            logs.pimain.info("%s SUCCESSFULLY WRITTEN TO DB", self.lilypod.name)
        else:
            logs.pimain.error("%s FAILED TO BE WRITTEN TO DB", self.lilypod.name)

    def read_sensor_data(self):
        dataPacket = self.serialcomm.read_serial()
        return dataPacket

    def run_spectroscopy(self):
        raise NotImplementedError()


def main():
    logs.pimain.info("LILYPOD MAIN START")
    lpodProc = LpodProc(u'lilypod_one')
    lpodProc.update_db(location=u'Toronto', ph=5.4, conductivity=8.5, spectroscopy={'low': 1, 'high': 2})


if __name__ == '__main__':
    main()
