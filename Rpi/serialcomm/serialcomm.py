from logs.logs import logs

import serial
from multiprocessing import Manager
import socket
import struct
import time


class CommManager():
    def __init__(self, host=socket.gethostname(), port=8082, protocol='serial'):
        self.procsManager = Manager()
        self.receiveQueue = self.procsManager.Queue(1)
        self.sendQueue = self.procsManager.Queue(1)
        if protocol == 'socket':
            self.host = host
            self.port = port
            self.address = (host, port)
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.address)


class Serialcomm:
    def __init__(self, baudrate=9600, slaveport='/dev/ttyACM0', protocol='serial'):
        self.commManager = CommManager(host=socket.gethostname(), port=8082, protocol='serial')
        self.messageLength = 10
        self.ser = serial.Serial(port=slaveport,
                                 baudrate=baudrate,
                                 timeout=1)

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

    def socket_send(self):
        try:
            while True:
                while self.commManager.sendQueue.qsize() <= 0:
                    pass
                if self.commManager.sendQueue.qsize() > 0:
                    commands = self.commManager.sendQueue.get()
                    commands.insert(0, float(12345.0))
                    commands.append(float(54321.0))
                    message = struct.pack('%sf' % len(commands), *commands)
                    self.send_msg(self.commManager.client, message)
                    logs.serialcomm.info("DATA SENT TO SERVER")
                    time.sleep(1)
        except Exception as e:
            logs.serialcomm.error("UNABLE TO SEND COMMANDS : %s", e)
            self.commManager.client.close()

    def socket_recv(self):
        try:
            while True:
                data = self.recv_msg(self.commManager.client)
                if not data:
                    raise ValueError
                decoded_data = struct.unpack('%sf' % (self.messageLength+2), data)
                if decoded_data[0] == 12345.0 and decoded_data[-1] == 54321.0:
                    self.commManager.receiveQueue.put(decoded_data)
                    logs.serialcomm.info("DATA PLACED IN RECEIVE QUEUE")
                    time.sleep(1)
                else:
                    logs.serialcomm.warning("WRONG START OR END BYTE, TRASHING DATA")
                    pass
        except Exception as e:
            logs.serialcomm.error("UNABLE TO RECEIVE COMMANDS : %s", e)
            self.commManager.client.close()

    def serial_send(self):
        try:
            while True:
                while self.commManager.sendQueue.qsize() <= 0:
                    pass
                if self.commManager.sendQueue.qsize() > 0:
                    commands = self.commManager.sendQueue.get()
                    # commands.insert(0, bytes.fromhex('FF'))
                    # commands.append(bytes.fromhex('FE'))
                    message = struct.pack('%sf' % (self.messageLength), *commands)
                    # print("Sending : ", message, " ", commands)
                    self.ser.write(bytes.fromhex('FA'))
                    self.ser.write(message)
                    self.ser.write(bytes.fromhex('FB'))
                    logs.serialcomm.info("DATA SENT TO SERVER")
                    # time.sleep(0.1)
        except Exception as e:
            logs.serialcomm.error("UNABLE TO SEND COMMANDS : %s", e)
            self.commManager.client.close()

    def serial_recv(self):
        try:
            while True:
                self.ser.reset_input_buffer()
                self.ser.read_until(bytearray.fromhex('FE'))
                rawData = self.ser.read(self.messageLength*4)
                endbyte = self.ser.read(1)
                if endbyte == bytearray.fromhex('FF'):
                    # print(rawData)
                    try:
                        decoded_data = struct.unpack('%sf' % (self.messageLength), rawData)
                        self.commManager.receiveQueue.put(decoded_data)
                        logs.serialcomm.info("DATA PLACED IN RECEIVE QUEUE")
                    except Exception as e:
                        logs.serialcomm.warning("UNABLE TO PLACE DATA IN RECEIVE QUEUE : %s", e)
                else:
                    logs.serialcomm.warning("WRONG START OR END BYTE, TRASHING DATA")
                    pass
                # time.sleep(0.1)
        except Exception as e:
            logs.serialcomm.error("UNABLE TO RECEIVE COMMANDS : %s", e)
            self.commManager.client.close()
