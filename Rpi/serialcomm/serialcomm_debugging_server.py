import socket
import struct
import random

messageLength = 10


def generateDummySensorData():
    floatlist = [random.random() for _ in range(messageLength)]
    floatlist.insert(0, 12345.0)
    floatlist.append(54321.0)
    sensordata = struct.pack('%sf' % len(floatlist), *floatlist)
    return sensordata


# Function to concatenate message that is received in pieces
def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


# Function to receive message through websocket
def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def send_msg(sock, msg):
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def server():
    host = socket.gethostname()
    port = 8082

    address = (host, port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)

    server.listen(5)
    conn, addr = server.accept()
    print("Connection from: " + str(addr))

    # floatlist = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    # message = struct.pack('%sf' % len(floatlist), *floatlist)
    # message = bytearray.fromhex('FF')
    while True:
        # data = self.recv_msg(client)
        try:
            data = recv_msg(conn)
            if not data:
                break
            decoded_data = struct.unpack('%sf' % (messageLength+2), data)
            print('Received from client: ', decoded_data)
            send_msg(conn, generateDummySensorData())
        except Exception:
            break
    conn.close()


if __name__ == "__main__":
    server()
