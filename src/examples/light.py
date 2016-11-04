import time
import RPi.GPIO as GPIO

light_pin = 16


def light():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(light_pin,GPIO.OUT)
    GPIO.output(light_pin,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.cleanup(light_pin)











