from Adafruit_PWM_Servo_Driver import PWM

from time import sleep

pwm = PWM(0x40)
pwm.setPWMFreq(50)
while True:
    pwm.setPWM(0,0,0)
    pwm.setPWM(1,0,0)