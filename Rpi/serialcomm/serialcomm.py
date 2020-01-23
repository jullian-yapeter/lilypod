import serial
import logging

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
        self.ser.reset_input_buffer()
        self.ser.read_until(bytearray.fromhex('FF'))