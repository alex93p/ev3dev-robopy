#!/usr/bin/env python3

# tipi di motore
BASE = 1
BRACCIO = 2
SOLLEVATORE = 3

# tipi di sensori
TOUCH = 1
COLOR = 2
ULTRASONIC = 3

# movimenti dei motori
CLOCKWISE = BACKWARD = DOWN = '+'
ANTICLOCKWISE = FORWARD = UP = '-'


# zero position
START_BASE = START_BRACCIO = START_SOLL = 0

# game position
GAME_BASE = -180 * 3
GAME_BRACCIO = 45 * 4
GAME_SOLLEVATORE = -90 * 24

# minime posizioni raggiungibili
MIN_BASE = -45 * 3
MIN_BRACCIO = 0 * 4
MIN_SOLLEVATORE = -10 * 24

# massime posizioni raggiungibili
MAX_BASE = -315 * 3
MAX_BRACCIO = 90 * 4
MAX_SOLLEVATORE = -160 * 24


