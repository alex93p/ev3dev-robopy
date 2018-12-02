#!/usr/bin/env python3

import socket
from _thread import *
from ev3dev2.socket_manager.deserializer import *


def thread_client(sock, conn):
    while 1:
        data = conn.recv(2048)
        msg = data.decode('utf-8')
        print('->', msg, '<-')
        if not data:
            waiting(sock)
        if msg == '#shutdown#':
            print(msg, '-> killing the socket!')
            sock.close()
        thread = Deserializer(conn, msg)
        thread.start()
    conn.close()

def thread_costumer(sock, conn):
    col = ColorSensor(INPUT_4)
    while 1:
        message = 'c' + '&' + str(col.reflected_light_intensity) + '&' + str(col.color_name)
        conn.send(str.encode(message))
        time.sleep(1)


def waiting(sock):
    while 1:
        conn, addr = sock.accept()
        print('# connected to: ' + addr[0] + ':' + str(addr[1]))
        start_new_thread(thread_client, (sock, conn,))
        start_new_thread(thread_costumer, (sock, conn,))


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
