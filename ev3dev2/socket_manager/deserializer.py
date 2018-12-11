#!/usr/bin/env python3

from threading import Thread
from _thread import *
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor import *
from ev3dev2.utility.degreeconverter import *
import ev3dev.ev3 as ev3
import random


class Deserializer (Thread):

    def __init__(self, sock, connection, message):
        Thread.__init__(self)
        self.sock = sock
        self.conn = connection
        self.message = message


    def run(self):
        self.deserialize()

    # deserializzatore per messaggi in ingresso nel canale
    def deserialize(self):

        if self.message[0] is '#' and self.message[-1] is '#' and self.message[1] is 'a':

            print ('thread has read:', self.message[2:-1])

            # se sto leggendo una richiesta di esecuzione di un motore
            if self.message[2] is 'e':
                self.runner_motor(self.motor_type_switcher.get(int(self.message[3])), option=self.message[4:])

            # sto leggendo una richiesta di configurazione torre
            elif self.message[2] is 'p':
                start_new_thread(self.thread_tower_builder_and_sender, ())

            # sto leggendo una richiesta di informazioni
            elif self.message[2] is 'r':
                # devo inviare i dati del sensore colore
                if self.message[3] is 'c':
                    start_new_thread(self.thread_check_color, ())
 
                # devo inviare un messaggio di informazioni di un sensore
                elif self.message[3] is 's':
                    self.getter_info(self.sensor_get_info_switcher.get(int(self.message[4])))

                # devo inviare un messaggio di debug
                elif self.message[3] is 'd':
                    debug = 'debug'

            # sto leggendo una richiesta per parlare
            elif self.message[2] is 't':
                msg = self.message[3:-1]
                ev3.Sound.speak(msg).wait()

        # il robot sta leggendo un messaggio corrotto
        else:
            print('WTF!! strange message:  ' + self.message)

    def thread_check_color(self):
        braccio = LargeMotor(OUTPUT_C)
        mano = MediumMotor(OUTPUT_D)
        ultra = UltrasonicSensor(INPUT_3)
        col = ColorSensor(INPUT_4)
        dist = round(ultra.distance_centimeters, 2)
        stop = False
        min_dist = 18.8
        max_dist = 19.3
        dir = -1
        if dist > max_dist:
            dir = 1
        braccio.on(SpeedPercent(dir * 10))
        while dist < min_dist or dist > max_dist:
            dist = round(ultra.distance_centimeters, 2)
        braccio.off()
        mano.on(SpeedPercent(50))
        while col.reflected_light_intensity == 0:
            continue
        mano.off()
        mano.on(SpeedPercent(10))
        color_name = 'No color'
        while color_name == 'No color' or color_name is None or color_name == 'None':
            color_name = self.control_color(col.reflected_light_intensity, col.color_name)
        mano.off()
        print(color_name)
        ev3.Sound.speak(color_name).wait()

    def control_color(self, luce, colore):
        if colore == 'Black':
            if 1 < luce < 7:
                return 'Black'
            else:
                return 'No color'
        elif colore == 'Blue':
            if luce < 15:
                return 'Blue'
            else:
                return 'No color'
        elif colore == 'Yellow':
            if luce > 25:
                return 'Yellow'
            else:
                return 'No color'
        elif colore == 'Red':
            if 10 < luce < 35:
                return 'Red'
            else:
                return 'No color'

    def thread_tower_builder_and_sender(self):
        pool = ['Black&', 'Black&', 'Blue&', 'Blue&', 'Yellow&', 'Yellow&', 'Red&', 'Red&']
        str_text = '#r&t&'
        end_text = '#'
        rand = random.sample(pool, 4)
        message = '' + str_text + rand[0] + rand[1] + rand[2] + rand[3] + end_text
        self.conn.send(str.encode(message))
        print('thread has sent back:', message)

    def thread_costumer(self):
        light = 0
        condition = True
        col = ColorSensor(INPUT_4)

        while condition:
            if col.reflected_light_intensity > light:
                light = col.reflected_light_intensity
            elif col.reflected_light_intensity == 0 and light > 0:
                condition = False
            
            message = 'c' + '&' + str(col.reflected_light_intensity) + '&' + str(col.color_name)
            print(message)
            self.conn.send(str.encode(message))
            time.sleep(0.3)

    def thread_distance(self):
        condition = True
        ultra = UltrasonicSensor(INPUT_3)

        while condition:
            message = 'g' + '&' + str(int(ultra.distance_centimeters))
            self.conn.send(str.encode(message))
            time.sleep(0.1)

            if int(ultra.distance_centimeters) == 19 or int(ultra.distance_centimeters) > 48:
                message = 'g' + '&' + str(19)
                print('distance: ', message)
                self.conn.send(str.encode(message))
                condition = False

    def thread_sender_info(self, string):
        self.conn.send(str.encode(string))

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
        base.on_for_degrees(SpeedPercent(speed), degrees_base(direction, quantity))
        start_new_thread(self.thread_sender_motor_info, (base.position // 3, BASE,))

    def motor_base_on(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        base = LargeMotor(OUTPUT_A)
        base.on(SpeedPercent(int(direction + str(speed))))

    def motor_base_off(self, option):
        base = LargeMotor(OUTPUT_A)
        base.off()

    def motor_braccio(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        braccio = LargeMotor(OUTPUT_C)
        braccio.on_for_degrees(SpeedPercent(speed), degrees_braccio(direction, quantity))
        start_new_thread(self.thread_sender_motor_info, (braccio.position // -4, BRACCIO,))

    def motor_braccio_on(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        braccio = LargeMotor(OUTPUT_C)
        braccio.on(SpeedPercent(int(direction + str(speed))))

    def motor_braccio_off(self, option):
        braccio = LargeMotor(OUTPUT_C)
        braccio.off()

    def motor_sollevatore(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        soll = MediumMotor(OUTPUT_D)
        soll.on_for_degrees(SpeedPercent(speed), degrees_sollevatore(direction, quantity))
        start_new_thread(self.thread_sender_motor_info, (soll.position // 24, SOLLEVATORE,))

    def motor_sollevatore_on(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        soll = MediumMotor(OUTPUT_D)
        soll.on(SpeedPercent(int(direction + str(speed))))

    def motor_sollevatore_off(self, option):
        soll = MediumMotor(OUTPUT_D)
        soll.off()

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

