#!/usr/bin/env python3

from ev3dev2.utility.global_variable import *


def degrees_sollevatore(direction, degrees):
    # comandi per il sollevatore
    command = 1
    conversion = 8600
    if direction is UP:
        command = -1
    return command*degrees*(conversion/360)


def degrees_braccio(direction, degrees):
    # comandi per il braccio
    command = 1
    conversion = 36
    if direction is FORWARD:
        command = -1
    return command*degrees*(conversion/360)


def degrees_base(direction, degrees):
    # comandi per la base
    command = -1
    if direction is CLOCKWISE:
        command = 1
    return command*degrees*(1085/360)
