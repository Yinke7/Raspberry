# !/bin/sh
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

LED_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

while True:
    try:
        GPIO.output(LED_PIN, not GPIO.input(LED_PIN))
        time.sleep(1)
        print("LED_PIN Level: %s" % GPIO.input(LED_PIN))
    except BaseException as e:
        print(e)
        break

print("GPIO.cleanup")
GPIO.cleanup()



