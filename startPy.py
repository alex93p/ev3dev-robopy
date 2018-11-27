#!/usr/bin/env python

import socket
from _thread import *
from ev3dev2.socket_manager.deserializer import *

host = ''
port = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))
s.listen(5)
print('# waiting for an input...\n')


def thread_client(conn):
    conn.send(str.encode('Welcome to the server...\n'))
    while 1:
        data = conn.recv(2048)
        msg = data.decode('utf-8')
        print('->', msg, '<-')
        if not data:
            waiting()
        thread = Deserializer(msg)
        thread.start()
        # reply = 'Server output: ' + msg
        # conn.sendall(str.encode(reply))
    conn.close()


def waiting(sock):
    while 1:
        conn, addr = sock.accept()
        print('# connected to: ' + addr[0] + ':' + str(addr[1]))
        start_new_thread(thread_client, (conn,))


waiting(s)
