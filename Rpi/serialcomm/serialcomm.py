import serial
import logging
from multiprocessing import Manager
import socket
import struct
import time

import binascii


class CommManager():
    def __init__(self, host=socket.gethostname(), port=8081):
        self.procsManager = Manager()
        self.receiveQueue = self.procsManager.Queue()
        self.sendQueue = self.procsManager.Queue()
        self.host = host
        self.port = port
        self.address = (host, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Serialcomm:
    def __init__(self, baudrate, slaveport='/dev/ttyACM0'):
        self.commManager = CommManager(host=socket.gethostname(), port=8082)
        self.numDataBytes = 10
        # self.ser = serial.Serial(
        #     port=slaveport,
        #     baudrate=baudrate,
        #     parity=serial.PARITY_NONE,
        #     stopbits=serial.STOPBITS_ONE,
        #     bytesize=serial.EIGHTBITS,
        #     timeout=1)

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

    # Function to concatenate message that is received in pieces
    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    # Function to receive message through websocket
    def recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(sock, msglen)

    def send_msg(self, sock, msg):
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    def socket_client(self):
        messageLength = self.numDataBytes
        self.commManager.client.connect(self.commManager.address)
        # floatlist = [1, 2, 3, 4, 5]
        # message = struct.pack('%sf' % len(floatlist), *floatlist)
        # message = bytearray.fromhex('FF')
        # message = b'1'
        while True:
            while self.commManager.sendQueue.qsize() <= 0:
                pass
            if self.commManager.sendQueue.qsize() > 0:
                message = self.commManager.sendQueue.get()
            self.send_msg(self.commManager.client, message)
            data = self.recv_msg(self.commManager.client)
            if not data:
                break
            decoded_data = struct.unpack('%sf' % messageLength, data)
            print('Received from server: ', decoded_data)
            time.sleep(1)
        self.commManager.client.close()


if __name__ == "__main__":
    serialcomm = Serialcomm(9600)
    serialcomm.socket_client()
