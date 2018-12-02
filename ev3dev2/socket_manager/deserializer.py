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

        # il robot sta leggendo un messaggio corrotto
        else:
            print('WTF!! strange message:  ' + self.message)

    def thread_sender_motor_info(self, conn, position, typem):
        message = '#r&' + 'm&' + str(typem) + '&' + str(position) + '&#'
        conn.send(str.encode(message))

    def thread_sender_sensor_info(self, conn, info, types):
        message = '#r&' + 's&' + str(types) + '&' + str(info) + '&#'
        conn.send(str.encode(message))

    def get_motor_option(self, option):
        direction = option[0]
        quantity = int(option[1:4]) - 110
        speed = int(option[4:7]) - 110
        return direction, quantity, speed

    def motor_base(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        base = LargeMotor(OUTPUT_A)
        base.on_for_degrees(SpeedPercent(speed), degrees_base(direction, quantity))
        start_new_thread(self.thread_sender_motor_info, (self.conn, base.position // 3, 1,))

    def motor_base_on(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        base = LargeMotor(OUTPUT_A)
        base.on(SpeedPercent(int(direction + str(speed))))

    def motor_base_off(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        base = LargeMotor(OUTPUT_A)
        base.off()

    def motor_braccio(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        braccio = LargeMotor(OUTPUT_C)
        braccio.on_for_degrees(SpeedPercent(speed), degrees_braccio(direction, quantity))
        start_new_thread(self.thread_sender_motor_info, (self.conn, braccio.position // -4, 2,))

    def motor_braccio_on(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        braccio = LargeMotor(OUTPUT_C)
        braccio.on(SpeedPercent(int(direction + str(speed))))

    def motor_braccio_off(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        braccio = LargeMotor(OUTPUT_C)
        braccio.off()

    def motor_sollevatore(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        soll = MediumMotor(OUTPUT_D)
        soll.on_for_degrees(SpeedPercent(speed), degrees_sollevatore(direction, quantity))
        start_new_thread(self.thread_sender_motor_info, (self.conn, soll.position // 24, 3,))

    def motor_sollevatore_on(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        soll = MediumMotor(OUTPUT_D)
        soll.on(SpeedPercent(int(direction + str(speed))))

    def motor_sollevatore_off(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        soll = MediumMotor(OUTPUT_D)
        soll.off()

    def sensor_touch(self):
        touch = TouchSensor(INPUT_1)
        start_new_thread(self.thread_sender_sensor_info, (self.conn, touch.is_pressed, 1,))

    def sensor_color(self):
        colore = ColorSensor(INPUT_2)
        start_new_thread(self.thread_sender_sensor_info, (self.conn, colore.color, 2,))

    def sensor_ultrasonic(self):
        ultra = UltrasonicSensor(INPUT_3)
        start_new_thread(self.thread_sender_sensor_info, (self.conn, ultra.distance_centimeters, 3,))

    def runner_motor(self, switch, option):
        func = switch
        func(self, option)

    def getter_info(self, switch):
        func = switch
        func(self)

    motor_type_switcher = {
        1: motor_base,
        2: motor_base_on,
        3: motor_base_off,
        4: motor_braccio,
        5: motor_braccio_on,
        6: motor_braccio_off,
        7: motor_sollevatore,
        8: motor_sollevatore_on,
        9: motor_sollevatore_off
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
