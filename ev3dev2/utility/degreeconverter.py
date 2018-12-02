#!/usr/bin/env python3

from ev3dev2.utility.global_variable import *


def degrees_sollevatore(direction, degrees):
    command = 1
    if direction is UP:
        command = -1
    return degrees * 24 * command


def degrees_braccio(direction, degrees):
    command = -1
    if direction is FORWARD:
        command = 1
    return degrees * 4 * command


def degrees_base(direction, degrees):
    command = -1
    if direction is CLOCKWISE:
        command = 1
    return degrees * 3 * command
