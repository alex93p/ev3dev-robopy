import time
import sys
from threading import Thread
from ev3dev2.utility.global_variable import *
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sound import *
from ev3dev2.led import *
from ev3dev2.utility.degreeconverter import *


class Deserializer (Thread):

    def __init__(self, message):
        Thread.__init__(self)
        self.message = str(message)[2:-1]

    def run(self):
        self.deserializer()

    # deserializzatore per messaggi in ingresso nel canale
    def deserializer(self):
        # se il messaggio è dall'app e sequence è corretto
        if self.message[0] is '#' and self.message[-1] is '#' and self.message[1] is 'a':
            # se sto leggendo una richiesta di esecuzione di un motore
            if self.message[2] is 'e':
                self.runner_motor(self.motor_type_switcher.get(int(self.message[3])), option=self.message[4:])
            # sto leggendo una richiesta di informazioni
            elif self.message[2] is 'r':
                # devo inviare un messaggio di informazioni di un motore
                if self.message[3] is 'm':
                    motor = 'motor'
                # devo inviare un messaggio di informazioni di un sensore
                elif self.message[3] is 's':
                    sensor = 'sensor'
        # il robot sta leggendo un suo messaggio
        else:
            print('WTF!! strange message:  ' + self.message)

    def get_motor_option(self, option):
        direction = option[0]
        quantity = int(option[1:4]) - 110
        speed = int(option[4:6]) - 110
        return direction, quantity, speed

    def motor_base(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        base = LargeMotor(OUTPUT_A)
        base.on_for_degrees(SpeedPercent(speed), degrees_base(direction, quantity))

    def motor_braccio(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        braccio = LargeMotor(OUTPUT_C)
        braccio.on_for_degrees(SpeedPercent(speed), degrees_braccio(direction, quantity))

    def motor_sollevatore(self, option):
        direction, quantity, speed = self.get_motor_option(option)
        soll = MediumMotor(OUTPUT_D)
        soll.on_for_degrees(SpeedPercent(speed), degrees_sollevatore(direction, quantity))

    def sensor_touch(self):
        return 1

    def sensor_color(self):
        return 1

    def sensor_ultrasonic(self):
        return 1

    def runner_motor(self, switch, option):
        func = switch
        func(self, option)

    motor_type_switcher = {
        1: motor_base,
        2: motor_braccio,
        3: motor_sollevatore
    }

    sensor_type_switcher = {
        4: sensor_touch,
        5: sensor_color,
        6: sensor_ultrasonic
    }


'''
negli indici delle stringhe abbiamo il primo numero compreso e il secondo escluso
ad esempio:
mess = '012345'
mess[0:2] = 01
'''


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
