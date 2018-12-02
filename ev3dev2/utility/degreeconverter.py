#!/usr/bin/env python3

from ev3dev2.utility.global_variable import *


def degrees_sollevatore(position, direction, degrees):
    # comandi per il sollevatore
    command = 1
    # conversion = 8600
    if direction is UP:
        command = -1
    degrees *= command
    if MAX_SOLLEVATORE <= (position + (degrees * 24)) <= MIN_SOLLEVATORE:
        return degrees * 24
    elif (position + (degrees * 24)) > MIN_SOLLEVATORE:
        return MIN_SOLLEVATORE - position
    else:
        return MAX_SOLLEVATORE - position


def degrees_braccio(position, direction, degrees):
    # comandi per il braccio
    command = -1
    # conversion = 1310
    if direction is FORWARD:
        command = 1
    degrees *= command
    if MIN_BRACCIO <= (position + (degrees * 4)) <= MAX_BRACCIO:
        return degrees * 4
    elif (position + (degrees * 4)) < MIN_BRACCIO:
        return MIN_BRACCIO - position
    else:
        return MAX_BRACCIO - position


def degrees_base(position, direction, degrees):
    # comandi per la base
    # conversion = 1085
    command = -1
    if direction is CLOCKWISE:
        command = 1
    degrees *= command
    if MAX_BASE <= (position + (degrees * 3)) <= MIN_BASE:
        return degrees * 3
    elif (position + (degrees * 3)) > MIN_BASE:
        return MIN_BASE - position
    else:
        return MAX_BASE - position
