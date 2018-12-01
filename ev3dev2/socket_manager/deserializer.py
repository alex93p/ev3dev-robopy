#!/usr/bin/env python3

from threading import Thread
from _thread import *
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor import *
from ev3dev2.utility.degreeconverter import *


class Deserializer (Thread):

    def __init__(self, connection, message):
        Thread.__init__(self)
        self.conn = connection
        self.message = message

    def run(self):
        self.deserialize()

    def go_to_Zero(self):
        base = LargeMotor(OUTPUT_A)
        braccio = LargeMotor(OUTPUT_C)
        soll = MediumMotor(OUTPUT_D)
        delta = - soll.position
        soll.on_for_degrees(SpeedPercent(100), delta)
        self.thread_sender_motor_info(soll.position, SOLLEVATORE)
        delta = - base.position
        base.on_for_degrees(SpeedPercent(75), delta)
        self.thread_sender_motor_info(base.position, BASE)
        delta = - braccio.position
        braccio.on_for_degrees(SpeedPercent(25), delta)
        self.thread_sender_motor_info(braccio.position, BRACCIO)

    def go_to_Start(self):
        base = LargeMotor(OUTPUT_A)
        braccio = LargeMotor(OUTPUT_C)
        soll = MediumMotor(OUTPUT_D)
        delta = (- soll.position) + GAME_SOLLEVATORE
        soll.on_for_degrees(SpeedPercent(100), delta)
        self.thread_sender_motor_info(soll.position, SOLLEVATORE)
        delta = (- base.position) + GAME_BASE
        base.on_for_degrees(SpeedPercent(75), delta)
        self.thread_sender_motor_info(base.position, BASE)
        delta = (- braccio.position) + GAME_BRACCIO
        braccio.on_for_degrees(SpeedPercent(25), delta)
        self.thread_sender_motor_info(braccio.position, BRACCIO)

    # deserializzatore per messaggi in ingresso nel canale
    def deserialize(self):

        if self.message[0] is '#' and self.message[-1] is '#' and self.message[1] is 'a':

            # se sto leggendo una richiesta di esecuzione di un motore
            if self.message[2] is 'e':
                self.runner_motor(self.motor_type_switcher.get(int(self.message[3])), option=self.message[4:])

            # sto leggendo una richiesta di informazioni
            elif self.message[2] is 'r':

                # devo inviare un messaggio di informazioni di un sensore
                if self.message[3] is 's':
                    self.getter_info(self.sensor_get_info_switcher.get(int(self.message[4])))

                # devo inviare un messaggio di debug
                elif self.message[3] is 'd':
                    debug = 'debug'
            elif self.message[2:-2] == 'zero':
                # funzione zero
                self.go_to_Zero()
            elif self.message[2:-2] == 'start':
                # funzione zero
                self.go_to_Start()

        # il robot sta leggendo un messaggio corrotto
        else:
            print('WTF!! strange message:  ' + self.message)

    def thread_sender_motor_info(self, position, typem):
        message = '#r&' + 'm&' + str(typem) + '&' + str(position) + '&#'
        self.conn.send(str.encode(message))

    def thread_sender_sensor_info(self, info, types):
        message = '#r&' + 's&' + str(types) + '&' + str(info) + '&#'
        self.conn.send(str.encode(message))

    def get_motor_option(self, option):
        direction = option[0]
        quantity = int(option[1:4]) - 110
        speed = int(option[4:7]) - 110
        return direction, quantity, speed

    def motor_base(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        base = LargeMotor(OUTPUT_A)
        base.on_for_degrees(SpeedPercent(speed), degrees_base(base.position, direction, quantity))
        start_new_thread(self.thread_sender_motor_info, (base.position // 3, BASE,))

    def motor_braccio(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        braccio = LargeMotor(OUTPUT_C)
        braccio.on_for_degrees(SpeedPercent(speed), degrees_braccio(direction, quantity))
        start_new_thread(self.thread_sender_motor_info, (braccio.position // -4, BRACCIO,))

    def motor_sollevatore(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        soll = MediumMotor(OUTPUT_D)
        soll.on_for_degrees(SpeedPercent(speed), degrees_sollevatore(direction, quantity))
        start_new_thread(self.thread_sender_motor_info, (soll.position // 24, SOLLEVATORE,))

    def sensor_touch(self):
        touch = TouchSensor(INPUT_1)
        start_new_thread(self.thread_sender_sensor_info, (touch.is_pressed, TOUCH,))

    def sensor_color(self):
        colore = ColorSensor(INPUT_2)
        start_new_thread(self.thread_sender_sensor_info, (colore.color, COLOR,))

    def sensor_ultrasonic(self):
        ultra = UltrasonicSensor(INPUT_3)
        start_new_thread(self.thread_sender_sensor_info, (ultra.distance_centimeters, ULTRASONIC,))

    def runner_motor(self, switch, option):
        func = switch
        func(self, option)

    def getter_info(self, switch):
        func = switch
        func(self)

    motor_type_switcher = {
        1: motor_base,
        2: motor_braccio,
        3: motor_sollevatore
    }

    sensor_get_info_switcher = {
        1: sensor_touch,
        2: sensor_color,
        3: sensor_ultrasonic
    }


'''

in quantità per ottenere il valore vero bisognerà sottrarre 110 al valore nel messaggio
in velocità per ottenere il valore vero bisognerà sottrarre 110 al valore nel messaggio
in posizione motore per ottenere il valore vero bisognerà sottrarre 180 al valore nel messaggio
dati sensori come li mappiamo ???

startoftext [1] '#' - android [1] 'a' - richiesta [1] 'r' - motore/sensore [1] 'm's' - tipo m/s [1] '1'..'6'- endoftext [1] '#'
                                      - esecuzione [1] 'e' - tipo motore [1] '1'2'3' - direzione [1] '+'-' - quantità [3] '181'..'320' - velocità [3] '111'..'210' - endoftext [1] '#'
                
startoftext [1] '#' - robot [1] 'r' - debug [1] 'd' - message - endoftext [1] '#'
                    - info [1] 'i' - motor [1] 'm' - tipo [1] '1'2'3' - posizione [3] '180'..'360'(minimo+180)(massimo+180) - endoftext [1] '#'
                                   - sensor [1] 's' - tipo [1] '4'5'6' - dato [4/8] 'dati' - endoftext [1] '#'

'''
