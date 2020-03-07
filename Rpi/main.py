import sys
import os
import psutil

from cloudcomm.cloudcomm import LilypodFirestore, LilypodObject
from serialcomm.serialcomm import Serialcomm
# from spectrometer.spectrometer import sample_water
from logs.logs import logs
from routine import LilypodRoutine
from cellular.geolocation import Geolocation
from multiprocessing import Process
import numpy as np
# import random
import time


def restart_program():
    time.sleep(1)
    print("----------------------------")
    print("-----RESTARTING PROGRAM-----")
    print("----------------------------")

    try:
        p = psutil.Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        logs.pimain.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)


class LpodProc():
    def __init__(self, name, baudrate=9600, slaveport='/dev/tty.usbmodem1421'):
        self.lilypod = LilypodObject(name=name, timestamp=0, location=[0.0, 0.0], ph=0.0, conductivity=0.0, garbageLevel=0.0,
                                     spectroscopy={'0': 0, '1': 0})
        self.lilypodFirestore = LilypodFirestore(dbName=u'lilypods')
        self.serialcomm = Serialcomm(baudrate=baudrate, slaveport=slaveport)
        self.routine = LilypodRoutine()
        self.geolocation = Geolocation()
        self.currData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def update_db(self, name=None, timestamp=None, location=None, ph=None, conductivity=None, garbageLevel=None, spectroscopy=None):
        if name is not None:
            self.lilypod.name = name
        if timestamp is not None:
            self.lilypod.timestamp = timestamp
        if location is not None:
            self.lilypod.location = location
        if ph is not None:
            self.lilypod.ph = ph
        if conductivity is not None:
            self.lilypod.conductivity = conductivity
        if garbageLevel is not None:
            self.lilypod.garbageLevel = garbageLevel
        if spectroscopy is not None:
            self.lilypod.spectroscopy = spectroscopy
        if (self.lilypodFirestore.write_to_db(self.lilypod)):
            logs.pimain.info("%s SUCCESSFULLY WRITTEN TO DB", self.lilypod.name)
        else:
            logs.pimain.error("%s FAILED TO BE WRITTEN TO DB", self.lilypod.name)

    def run_spectroscopy(self):
        # Dummy Spectrometer Data
        return {"0": np.random.uniform(0, 100), "1": np.random.uniform(0, 100), "2": np.random.uniform(0, 100), "3": np.random.uniform(0, 100), "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": np.random.uniform(0, 100)}
        # return sample_water()

    def generateDummyCommandsData(self):
        while self.serialcomm.commManager.sendQueue.qsize() > 0:
            pass
        # COMMANDS FORMAT:
        # commands = [pumpState, bulbState, garageState, garageDir, trapState,
        #             trapDir, phState, condState, ussState, ledStrip]
        # FOR RANDOM COMMANDS:
        # commands = [random.random() for _ in range(self.serialcomm.messageLength)]
        self.routine.updateState('CHECKGARBAGE')
        commands = self.routine.currentRoutineStep
        return commands

    def generateCommandsData(self, sensorData, prevState, currElapsedTime):
        # COMMANDS FORMAT:
        # commands = [pumpState, bulbState, garageState, garageDir, trapState,
        #             trapDir, phState, condState, ussState, ledStrip]
        # print("CURR ELAPSED TIME :", currElapsedTime)
        startTime = time.time()
        # while self.serialcomm.commManager.sendQueue.qsize() > 0:
        #     self.serialcomm.commManager.sendQueue.get()
        if currElapsedTime < self.routine.timingLookUp[prevState]:
            self.routine.updateState(prevState)
            commands = self.routine.currentRoutineStep
            return currElapsedTime + time.time() - startTime, prevState, commands
        else:
            # newGarageState = sensorData[0]
            # phValue = sensorData[2]
            # condValue = sensorData[3]
            try:
                newTrapState = sensorData[1]
                ussValue = sensorData[4]
            except Exception as e:
                logs.pimain.warning("USSValue was NoneType: %s", e)
                pass
            if prevState == 'CHECKGARBAGE':
                if round(ussValue, 2) == 1.0:
                    newState = 'GARBAGEFULL'
                else:
                    newState = 'FILTERSTATE'
            if prevState == 'FILTERSTATE':
                if (round(newTrapState, 2) == 1.0) or (round(newTrapState, 2) == 0.0):
                    newState = 'SAMPLESTATE'
                elif round(newTrapState, 2) == 2.0:
                    newState = 'MALFUNCTION'
            if prevState == 'SAMPLESTATE':
                newState = 'CHECKGARBAGE'
            self.routine.updateState(newState)
            commands = self.routine.currentRoutineStep
            return 0, newState, commands

    def send_to_arduino(self, state, commands):
        # while self.serialcomm.commManager.sendQueue.qsize() > 0:
        #     self.serialcomm.commManager.sendQueue.get()
        if self.serialcomm.commManager.sendQueue.qsize() > 0:
            logs.pimain.info("ARDUINO BUSY, TRASH COMMAND")
            return False
        elif self.serialcomm.commManager.sendQueue.qsize() == 0:
            self.serialcomm.commManager.sendQueue.put(commands)
            logs.pimain.info("COMMANDS PLACED IN QUEUE")
            return True
        # else:
        #     logs.pimain.info("ARDUINO BUSY, TRASH COMMAND")

    def read_from_arduino(self):
        if self.serialcomm.commManager.receiveQueue.qsize() <= 0:
            return False, None
        # dataNotReceived = True
        # while dataNotReceived:
        #     if self.serialcomm.commManager.receiveQueue.qsize() > 0:
        #         dataNotReceived = False
        elif self.serialcomm.commManager.receiveQueue.qsize() > 0:
            self.currData = self.serialcomm.commManager.receiveQueue.get()
            logs.pimain.info("DATA POPPED FROM QUEUE")
            return True, self.currData
        # else:
        #     return None


def main():
    logs.pimain.info("LILYPOD MAIN START")
    lpodProc = LpodProc(name=u'lilypod_two', baudrate=9600, slaveport='/dev/cu.usbmodem1411')
    # Socket version for debugging
    # sendProc = Process(target=lpodProc.serialcomm.socket_send)
    # recvProc = Process(target=lpodProc.serialcomm.socket_recv)
    # # Serial version for real application
    sendProc = Process(target=lpodProc.serialcomm.serial_send)
    recvProc = Process(target=lpodProc.serialcomm.serial_recv)

    sendProc.start()
    time.sleep(0.1)
    recvProc.start()
    time.sleep(0.1)

    # This represents the main functions of the Raspberry Pi
    prevState = 'CHECKGARBAGE'
    prevTime = 0
    procTime = 0
    phValue = 0
    condValue = 0
    sensorData = []
    start = time.time()
    try:
        while (True):#(time.time() - start < 500):
            # commands = lpodProc.generateDummyCommandsData()
            prevTime, prevState, commands = lpodProc.generateCommandsData(lpodProc.currData, prevState, prevTime + procTime)
            startProcTime = time.time()
            successfulcommunication = False

            datasent = False
            datareceived = False
            while not successfulcommunication:
                datasent = lpodProc.send_to_arduino(prevState, commands)
                datareceived, sensorData = lpodProc.read_from_arduino()
                if (sensorData is not None) and (None not in sensorData):
                    successfulcommunication = True

            pumpState = commands[0]
            bulbState = commands[1]
            garageState = commands[2]
            garageDir = commands[3]
            trapState = commands[4]
            trapDir = commands[5]
            phState = commands[6]
            condState = commands[7]
            ussState = commands[8]
            ledStrip = commands[9]
            print("ROUTINE : ", prevState)
            print("Sent to Arduino : [{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f}]"
                .format(pumpState, bulbState, garageState, garageDir, trapState, trapDir, phState, condState, ussState, ledStrip))

            lpodProc.currData = sensorData
            newGarageState = sensorData[0]
            newTrapState = sensorData[1]
            if sensorData[2] > 0:
                phValue = sensorData[2]
            if sensorData[3] > 0:
                condValue = sensorData[3]
            ussValue = sensorData[4]
            bulbValue = sensorData[5]
            ledValue = sensorData[6]
            print("Received from Arduino : [{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f}]"
                    .format(newGarageState, newTrapState, phValue, condValue, ussValue, bulbValue, ledValue))
            # Process data and update database
            if prevState == 'SAMPLESTATE':
                lpodProc.update_db(location=lpodProc.geolocation.getGeolocation(), timestamp=time.time(),
                                    ph=round(phValue, 2), conductivity=round(condValue, 2),
                                    garbageLevel=round(ussValue, 2), spectroscopy=lpodProc.run_spectroscopy())
            procTime = time.time() - startProcTime
    except Exception as e:
        logs.pimain.error("MAIN PROCESS FAILED DUE TO %s", e)
        logs.pimain.error("RESTARTING PROGRAM")
        restart_program()

    sendProc.terminate()
    recvProc.terminate()
    sendProc.join()
    recvProc.join()


if __name__ == '__main__':
    main()
