import serial
import logging

import binascii

logging.basicConfig(level=logging.INFO, file='logs/piserialcomm.log')


class Serialcomm:
    def __init__(self, baudrate, slaveport='/dev/ttyACM0'):
        self.numDataBytes = 6
        self.ser = serial.Serial(
            port=slaveport,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

    def readSerial(self):
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
        return dataPacket
