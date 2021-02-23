# !/bin/sh
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys

LED_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
while True:
    try:
        GPIO.output(LED_PIN, not GPIO.input(LED_PIN))
        time.sleep(1)
        print("LED_PIN Level: %s" % GPIO.input(LED_PIN))
    except KeyboardInterrupt as err:
        print(err)
        break

print("GPIO.cleanup")
GPIO.cleanup()


