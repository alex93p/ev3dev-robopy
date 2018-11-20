#!/usr/bin/env python3

import socket
import sys
from ev3dev2.socket.deserializer import Deserializer

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)  # ip localhost EV3
PORT = 8888  # port localhost EV3
print('Host IP: ' + HOST)

# creiamo il socket per aprire il canale di comunicazione con `socket.socket`
# socket.AF_INET -> Address Format, Internet = IP Addresses
# socket.SOCK_STREAM -> comunicazione duplex (lettura / scrittura byte sul canale)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Socket Created!')

# Bindiamo il socket all'host e alla porta
try:
    s.bind((HOST, PORT))
except socket.error as err:
    s.detach()
    s.close()
    print('Bind Failed -> Error Code: ' + str(err[0]) + ', Message: ' + err[1])
    sys.exit()
print('Socket Bind Success!')


# Mettiamo in ascolto il socket con `listen(10)` -> 10: protocollo TCP
s.listen(10)
print('Socket is listening...')

# conn, addr = s.accept()
# print('Connect with ' + addr[0] + ':' + str(addr[1]))
# Restiamo in ascolto sempre


while 1:
    conn, addr = s.accept()
    print('Connect with ' + addr[0] + ':' + str(addr[1]))

    # mettiamo in un buffer quello che riceviamo dal socket -> 32: max byte / default 1024
    buf = conn.recv(32)
    if buf is not None:
        thread_message = Deserializer(buf)
        thread_message.start()
    print(buf)
s.detach()
s.close()
