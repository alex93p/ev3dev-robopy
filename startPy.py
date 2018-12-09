#!/usr/bin/env python3

import socket
from _thread import *
from ev3dev2.socket_manager.deserializer import *


def tower_builder():
    pool = ['Black&', 'Black&', 'Blue&', 'Blue&', 'Yellow&', 'Yellow&', 'Red&', 'Red&']
    str_text = '#r&t&'
    end_text = '#'
    rand = random.sample(pool, 4)
    mess = '' + str_text + rand[0] + rand[1] + rand[2] + rand[3] + end_text
    return mess

def thread_client(sock, conn):
    global users
    while 1:
        data = conn.recv(2048)
        msg = data.decode('utf-8')
        print('->', msg, '<-')
        if not data:
            users -= 1
            waiting(sock)
        if msg == '#shutdown#':
            print(msg, '-> killing the socket!')
            sock.close()
        thread = Deserializer(sock, conn, msg)
        thread.start()
    conn.close()


def waiting(sock):
    global users
    global message
    while 1:
        conn, addr = sock.accept()
        users += 1
        if users == 1:
            message = tower_builder()
            conn.send(str.encode(message))
        elif users == 2:
            conn.send(str.encode(message))
        print('# connected to: ' + addr[0] + ':' + str(addr[1]))
        start_new_thread(thread_client, (sock, conn,))


message = ''
users = 0
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
