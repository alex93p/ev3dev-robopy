#!/usr/bin/env python3

# esempi di frame:

# sequenza messaggi
SEQUENCE = 0

# messaggi con seq diversi
MESSAGE_IN_QUE = []

# tipi di motore
BASE = 1
BRACCIO = 2
SOLLEVATORE = 3

# tipi di sensori
TOUCH = 4
COLOR = 5
ULTRASONIC = 6

# movimenti dei motori
CLOCKWISE = BACKWARD = DOWN = '+'
ANTICLOCKWISE = FORWARD = UP = '-'


# zero position
START_BASE = START_BRACCIO = START_SOLL = 0
# minime posizioni raggiungibili
MIN_BASE = 0
MIN_BRACCIO = 0
MIN_SOLLEVATORE = 0

# massime posizioni raggiungibili
MAX_BASE = 270 * 3
MAX_BRACCIO = 90 * 4
MAX_SOLLEVATORE = 180 * 24

# informazioni dei sensori ??


def append_message(message):
    global MESSAGE_IN_QUE
    MESSAGE_IN_QUE += message


def upgrade_seq():
    global SEQUENCE
    SEQUENCE += 1


def set_seq_to_zero():
    global SEQUENCE
    SEQUENCE = 0
