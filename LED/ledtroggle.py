# !/bin/sh
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys

LED_PIN = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
while True:
    try:
        GPIO.output(LED_PIN, not GPIO.input(LED_PIN))
        time.sleep(1)

    except BaseException as err:
        print(err)
        break

GPIO.cleanup()


