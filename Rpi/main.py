from cloudcomm.cloudcomm import LilypodFirestore, LilypodObject
from serialcomm.serialcomm import Serialcomm
# from spectrometer import spectrometer
from logs.logs import logs

from multiprocessing import Process
import random
import struct
import time


class LpodProc():
    def __init__(self, name):
        self.lilypod = LilypodObject(name=name, location=u'Waterloo', ph=0.0, conductivity=0.0,
                                     spectroscopy={'low': 0, 'high': 0})
        self.lilypodFirestore = LilypodFirestore(dbName=u'lilypods')
        self.serialcomm = Serialcomm(9600)
        self.currData = None

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

    def read_from_arduino(self):
        while self.commManager.receiveQueue.qsize() <= 0:  # Wait until the first image is pushed to the queue
            pass
        if self.commManager.receiveQueue.qsize() > 0:
            self.currData = self.commManager.receiveQueue.get()

    def send_to_arduino(self, commands):
        self.serialcomm.commManager.sendQueue.put(commands)
        logs.pimain.info("COMMANDS PLACED IN QUEUE")

    def run_spectroscopy(self):
        raise NotImplementedError()

    def generateDummySensorData(self):
        while True:
            while self.serialcomm.commManager.sendQueue.qsize() > 0:
                pass
            floatlist = [random.random() for _ in range(10)]
            commands = struct.pack('%sf' % len(floatlist), *floatlist)
            self.serialcomm.commManager.sendQueue.put(commands)


def main():
    logs.pimain.info("LILYPOD MAIN START")
    lpodProc = LpodProc(u'lilypod_one')
    receiveProc = Process(target=lpodProc.serialcomm.read_serial)
    sendProc = Process(target=lpodProc.serialcomm.write_serial)
    receiveProc.start()
    sendProc.start()
    try:
        while True:
            lpodProc.update_db(location=u'Toronto', ph=5.4, conductivity=8.5, spectroscopy={'low': 1, 'high': 2})
    except Exception as e:
        logs.pimain.error("MAIN PROCESS FAILED DUE TO %s", e)
        receiveProc.terminate()
        sendProc.terminate()
        receiveProc.join()
        sendProc.join()


if __name__ == '__main__':
    lpodProc = LpodProc(u'lilypod_one')
    dummydataProc = Process(target=lpodProc.generateDummySensorData)
    clientProc = Process(target=lpodProc.serialcomm.socket_client)
    dummydataProc.start()
    clientProc.start()
    time.sleep(10)
    dummydataProc.terminate()
    clientProc.terminate()
    dummydataProc.join()
    clientProc.join()
