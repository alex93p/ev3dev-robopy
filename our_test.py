#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sound import *
from ev3dev2.led import *
import socket
import sys
import time

print("i'm ready to spin...")

touch = TouchSensor(INPUT_1)
sollevatore = MediumMotor(OUTPUT_D)


def degrees_sollevatore(degrees, direction):
    # comandi per il sollevatore
    up = 'up'
    down = 'down'
    command = -1
    conversion = 8600
    if direction is up:
        command = 1
    return command*degrees*(conversion/360)


def wait():
    while not touch.is_pressed:
        time.sleep(0.01)


while 1:
    wait()
    # sollevatore.on_for_degrees(SpeedPercent(50), degrees_sollevatore(1, 'up'))
    sollevatore.on_for_degrees(SpeedPercent(100), degrees_sollevatore(1, 'down'))
