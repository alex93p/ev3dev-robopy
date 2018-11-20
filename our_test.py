#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sound import *
from ev3dev2.led import *
from ev3dev2.utility.degreeconverter import *
import socket
import sys
import time

print("i'm ready to spin...")

t_down = TouchSensor(INPUT_2)
t_up = TouchSensor(INPUT_1)

braccio = LargeMotor(OUTPUT_C)
dir = FORWARD


def get_swith(switcher):
    func = switcher
    func()


def up():
    braccio.on_for_degrees(SpeedPercent(100), degrees_braccio(BACKWARD, 3))


def down():
    braccio.on_for_degrees(SpeedPercent(100), degrees_braccio(FORWARD, 3))


switch = {
    FORWARD: down,
    BACKWARD: up
}

while 1:
    timeit = 0
    flag = 0
    while not t_down.is_pressed and not t_up.is_pressed:
        time.sleep(0.01)
    if t_down.is_pressed:
        print('DOWN pressed')
        dir = FORWARD
    elif t_up.is_pressed:
        print('UP pressed')
        dir = BACKWARD
    get_swith(switch.get(dir))
