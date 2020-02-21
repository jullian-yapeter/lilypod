from cloudcomm.cloudcomm import LilypodFirestore, LilypodObject
from serialcomm.serialcomm import Serialcomm
# from spectrometer import spectrometer
from logs.logs import logs

from multiprocessing import Process
import random
import time


class LpodProc():
    def __init__(self, name, baudrate=9600, slaveport='/dev/tty.usbmodem1421'):
        self.lilypod = LilypodObject(name=name, location=u'Waterloo', ph=0.0, conductivity=0.0,
                                     spectroscopy={'low': 0, 'high': 0})
        self.lilypodFirestore = LilypodFirestore(dbName=u'lilypods')
        self.serialcomm = Serialcomm(baudrate=baudrate, slaveport=slaveport)
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

    def run_spectroscopy(self):
        raise NotImplementedError()

    def generateDummyCommandsData(self):
        while self.serialcomm.commManager.sendQueue.qsize() > 0:
            pass
        # commands = [random.random() for _ in range(self.serialcomm.messageLength)]
        commands = [10.0, 9.0, 8.0, 7.0, 3.0, 5.0, 4.0, 3.0, 2.0, 1.0]
        # commands = [123]
        return commands

    def send_to_arduino(self, commands):
        self.serialcomm.commManager.sendQueue.put(commands)
        logs.pimain.info("COMMANDS PLACED IN QUEUE")

    def read_from_arduino(self):
        if self.serialcomm.commManager.receiveQueue.qsize() <= 0:
            return None
        if self.serialcomm.commManager.receiveQueue.qsize() > 0:
            self.currData = self.serialcomm.commManager.receiveQueue.get()
            logs.pimain.info("DATA POPPED FROM QUEUE")
            return self.currData


def main():
    logs.pimain.info("LILYPOD MAIN START")
    lpodProc = LpodProc(name=u'lilypod_one', baudrate=9600, slaveport='/dev/tty.usbmodem1411')
    # Socket version for debugging
    # sendProc = Process(target=lpodProc.serialcomm.socket_send)
    # recvProc = Process(target=lpodProc.serialcomm.socket_recv)
    # # Serial version for real application
    sendProc = Process(target=lpodProc.serialcomm.serial_send)
    recvProc = Process(target=lpodProc.serialcomm.serial_recv)
    # recvloopProc = Process(target=lpodProc.serialcomm.serial_recv_loop)

    sendProc.start()
    time.sleep(0.1)
    recvProc.start()
    # recvloopProc.start()
    time.sleep(0.1)

    # This represents the main functions of the Raspberry Pi
    start = time.time()
    try:
        while (time.time() - start < 10):
            commands = lpodProc.generateDummyCommandsData()
            lpodProc.send_to_arduino(commands)
            # print(commands)
            sensordata = lpodProc.read_from_arduino()
            if sensordata:
                print("Received from server : ", sensordata)
            # Process data and update database
            lpodProc.update_db(location=u'Toronto', ph=2.4, conductivity=8.8, spectroscopy={'low': 2, 'high': 2})
    except Exception as e:
        logs.pimain.error("MAIN PROCESS FAILED DUE TO %s", e)

    sendProc.terminate()
    recvProc.terminate()
    # recvloopProc.terminate()
    sendProc.join()
    recvProc.join()
    # recvloopProc.terminate()


if __name__ == '__main__':
    main()
