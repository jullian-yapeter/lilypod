import serial
import logging
from multiprocessing import Manager

import binascii


class CommManager:
    receiveManager = Manager()
    receiveQueue = receiveManager.Queue()
    sendManager = Manager()
    sendQueue = sendManager.Queue()


class Serialcomm:
    def __init__(self, baudrate, slaveport='/dev/ttyACM0'):
        self.commManager = CommManager()
        self.numDataBytes = 6
        self.ser = serial.Serial(
            port=slaveport,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

    def read_serial(self):
        while True:
            dataPacket = []
            self.ser.reset_input_buffer()
            self.ser.read_until(bytearray.fromhex('FF'))
            rawDataPacket = self.ser.read(self.numDataBytes)
            endByte = self.ser.read(1)
            if endByte == bytearray.fromhex('FE'):
                for i in range(self.numDataBytes):
                    dataByte = rawDataPacket[i]
                    dataHex = binascii.hexlify(dataByte)
                    dataDec = int(dataHex, 16)
                    dataPacket.append(dataDec)
            else:
                logging.error("WRONG ENDBYTE")
            self.commManager.receiveQueue.put(dataPacket)

    def write_serial(self, commands):
        while True:
            while self.commManager.sendQueue.qsize() <= 0:  # Wait until the first image is pushed to the queue
                pass
            if self.commManager.sendQueue.qsize() > 0:
                commands = self.commManager.sendQueue.get()
                commandToSend = commands
                commandToSend.append(hex(int('ff', 16)), 0)
                commandToSend.append(hex(int('fe', 16)), -1)
                self.ser.write(bytearray(commandToSend))
                logging.info("COMMANDS SENT")
