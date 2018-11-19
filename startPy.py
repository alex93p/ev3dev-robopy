#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sound import *
from ev3dev2.led import *
import socket
import sys
from ev3dev2.utility.global_variable import *
from ev3dev2.socket.deserializer import Deserializer


def degrees_sollevatore(degrees, direction):
    # comandi per il sollevatore
    command = 1
    conversion = 8600
    if direction is UP:
        command = -1
    return command*degrees*(conversion/360)


def degrees_braccio(degrees, direction):
    # comandi per il braccio
    command = 1
    conversion = 36
    if direction is FORWARD:
        command = -1
    return command*degrees*(conversion/360)


def degrees_base(degrees, direction):
    # comandi per la base
    command = -1
    if direction is CLOCKWISE:
        command = 1
    return command*degrees*(1085/360)


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
    # if buf is not null
    thread_message = Deserializer(buf)
    thread_message.start()
    '''
    base = LargeMotor(OUTPUT_A)
    # senso orario
    base.on_for_degrees(SpeedPercent(30), degrees_base(120, CLOCKWISE))
    # senso antiorario
    # base.on_for_degrees(SpeedPercent(100), -360)
    braccio = LargeMotor(OUTPUT_C)
    braccio.on_for_degrees(SpeedPercent(10), degrees_base(20, FORWARD))
    sollevatore = MediumMotor(OUTPUT_D)
    # sollevatore.on_for_degrees(SpeedPercent(100), convert_degrees_motor_base(1000, DOWN))

    # sollevatore.on_for_degrees(SpeedPercent(1), convert_degrees_motor_base(100, UP))
    braccio.on_for_degrees(SpeedPercent(15), degrees_base(20, BACKWARD))
    base.on_for_degrees(SpeedPercent(60), degrees_base(120, ANTICLOCKWISE))
    '''
    '''
    steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
    t4 = TouchSensor(INPUT_1)
    steering_drive.on(0, SpeedPercent(100))
    color_sens = ColorSensor(INPUT_3)
    tavolo = color_sens.color
    while color_sens.color is tavolo and not t4.is_pressed:
        if not t4.is_released:
            break
        continue
    steering_drive.stop()
    sound = Sound()
    sound.speak('oh fuck fuck fuck!')
    steering_drive.on_for_degrees(0, SpeedPercent(100), -1)
    steering_drive.on_for_rotations(0, SpeedPercent(20), -1)
    # rotazione 180 gradi
    tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
    tank_drive.on_for_rotations(50, -50, 1)
            for motor in list_motors():
        motor.on_for_rotations(SpeedPercent(10), 3)
        continue
    la = LargeMotor(OUTPUT_A)
    la.on_for_rotations(SpeedPercent(10), 3)
    print('primo motore..')
    lb = LargeMotor(OUTPUT_B)
    lb.on_for_rotations(SpeedPercent(10), 3)
    print('secondo motore..')
    sc = MediumMotor(OUTPUT_C)
    sc.on_for_degrees(SpeedPercent(100), 1000)
    print('terzo motore..')
    t4 = TouchSensor(INPUT_1)
    touched = False
    while not touched:
        touched = t4.is_pressed
    print('sensore toccato..')
    '''
    print(buf)
s.close()
