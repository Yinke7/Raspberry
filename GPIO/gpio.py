# !/bin/python3
# -*- coding: utf-8 -*-

""" Pi 4B GPIO mapping:

 +-----+-----+---------+------+---+---Pi 4B--+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
 |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5v      |     |     |
 |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |
 |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 1 | IN   | TxD     | 15  | 14  |
 |     |     |      0v |      |   |  9 || 10 | 1 | IN   | RxD     | 16  | 15  |
 |  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
 |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |
 |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
 |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
 |  10 |  12 |    MOSI | ALT0 | 0 | 19 || 20 |   |      | 0v      |     |     |
 |   9 |  13 |    MISO | ALT0 | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
 |  11 |  14 |    SCLK | ALT0 | 1 | 23 || 24 | 1 | OUT  | CE0     | 10  | 8   |
 |     |     |      0v |      |   | 25 || 26 | 1 | OUT  | CE1     | 11  | 7   |
 |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
 |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |
 |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
 |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |
 |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
 |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 1 | IN   | GPIO.28 | 28  | 20  |
 |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+---Pi 4B--+---+------+---------+-----+-----+

@reference: https://tieske.github.io/rpi-gpio/modules/GPIO.html
"""

import RPi.GPIO as GPIO
import time
import threading



IRQ_PIN = 17
LED1_PIN = 18
LED2_PIN = 27


def Toggle(pin, repeat):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    if repeat:
        while True:
            try:
                GPIO.output(pin, not GPIO.input(pin))
                time.sleep(1)
                print("BCM[%d] Level: %d" % (pin, not GPIO.input(pin)))
            except BaseException as e:
                print(e)
                break
    else:
        GPIO.output(pin, not GPIO.input(pin))
        print("BCM[%d] Level: %s" % (pin, GPIO.input(pin)))

    GPIO.cleanup(pin)
    return


def Readpin(pin):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
    while True:
        try:
            res = GPIO.wait_for_edge(pin, GPIO.FALLING, bouncetime=200)
            if pin == res:
                print("interrupt")
                Toggle(LED2_PIN, False)
            else:
                print("timeout")
        except BaseException as exp:
            print(exp)
            break

    GPIO.cleanup(pin)
    return


if __name__ == "__main__":
    try:
        thread = []
        t1 = threading.Thread(target=Toggle, args=(LED1_PIN, True, ), name="led1")
        thread.append(t1)
        t2 = threading.Thread(target=Readpin, args=(IRQ_PIN, ), name="irq")
        thread.append(t2)

        for t in thread:
            t.setDaemon(True)
            t.start()
        for t in thread:
            t.join()

    except BaseException as exp:
        print(exp)

