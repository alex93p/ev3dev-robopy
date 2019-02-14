#!/usr/bin/env python3

import socket
from _thread import *

host = '192.168.43.51'
port = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))
s.listen(5)
print('# server IP:', socket.gethostbyname(socket.gethostname()), '\n')
print('# waiting for an input...\n')

def thread_client(sock, conn):
    # conn.send(str.encode('Welcome to the server...\n'))
    while 1:
        data = conn.recv(2048)
        msg = data.decode('utf-8')
        # scommentare solo quando uso telnet da terminale
        # msg = msg[0:-2]
        print('->', msg, '<-')
        if not data:
            waiting()
        if msg == '#aplayer#':
            message = '#r&t&Red&Yellow&Blue&Red&#'
            conn.send(str.encode(message))
        if msg == '#arc#':
            message = '#r&c&Red&#'
            conn.send(str.encode(message))
        if msg == '#apstop#':
            message = '#r&t&Red&Yellow&Blue&Red&#'
            conn.send(str.encode(message))
        if msg == '#shutdown#':
            print(msg, '-> killing the socket!')
            sock.close()
    conn.close()


def waiting(sock):
    while 1:
        conn, addr = sock.accept()
        print('# connected to: ' + addr[0] + ':' + str(addr[1]))
        # message = '#r&t&Red&Yellow&Blue&Red&#'
        # print(message)
        # conn.send(str.encode(message))
        start_new_thread(thread_client, (sock, conn,))


waiting(s)

# colori
# socket aperto
