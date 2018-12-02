#!/usr/bin/env python3

import socket
from _thread import *
from ev3dev2.socket_manager.deserializer import *


def thread_client(sock, conn):
    conn.send(str.encode('Welcome to the server...\n'))
    col = ColorSensor(INPUT_4)
    ultra = UltrasonicSensor(INPUT_3)
    col.calibrate_white()
    while 1:
        data = conn.recv(2048)
        msg = data.decode('utf-8')
        print('->', msg, '<-')
        print('color:', col.color, col.color_name)
        print('dist:', ultra.distance_centimeters)
        if not data:
            waiting(sock)
        if msg == '#shutdown#':
            print(msg, '-> killing the socket!')
            sock.close()
        thread = Deserializer(conn, msg)
        thread.start()
    conn.close()


def waiting(sock):
    while 1:
        conn, addr = sock.accept()
        print('# connected to: ' + addr[0] + ':' + str(addr[1]))
        start_new_thread(thread_client, (sock, conn,))


host = ''
port = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))
s.listen(10)
print('# server IP:', socket.gethostbyname(socket.gethostname()), '\n')
print('# waiting for an input...\n')
waiting(s)
