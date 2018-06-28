#!/usr/bin/python
from Adafruit_PWM_Servo_Driver import PWM

class Robot(object):
    def __init__(self,address,freq):
        self.pwm = PWM(address)
        self.pwm.setPWMFreq(freq)
    def drive(self, left, right):
        self.pwm.setPWM(0, 0, int(left))
        self.pwm.setPWM(1, 0, int(right))
