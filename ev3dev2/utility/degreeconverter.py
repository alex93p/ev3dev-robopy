#!/usr/bin/env python3

from ev3dev2.utility.global_variable import *


def degrees_sollevatore(direction, degrees):
    # comandi per il sollevatore
    command = 1
    # conversion = 8600
    if direction is UP:
        command = -1
    return command*degrees*24


def degrees_braccio(direction, degrees):
    # comandi per il braccio
    command = -1
    # conversion = 1310
    if direction is FORWARD:
        command = 1
    return command*degrees*4


def degrees_base(position, direction, degrees):
    # comandi per la base
    # conversion = 1085
    command = -1
    if direction is CLOCKWISE:
        command = 1
    degrees *= command
    if MIN_BASE <= (position + (degrees * 3)) <= MAX_BASE:
        return degrees * 3
    elif (position + (degrees * 3)) < MIN_BASE:
        return MIN_BASE - position
    else:
        return (MAX_BASE - position) * 3
