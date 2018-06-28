#!/usr/bin/python
import myoband
import emotiv as nt
import robot

from time import sleep


bot = robot.Robot(0x40, 50)
bot.drive(0,0)

my = myoband.Myoband()
my.initialize()

nt.isConcentrating = None
print("MyoBand Connected")
while True:
    my.start()
    left, right = my.motor_speeds()
    if nt.isConcentrating == None:
        bot.drive(left, right)
        print("Not Connected... Left: " + str(left) + "; Right: " + str(right))
    if nt.isConcentrating == True:
        bot.drive(left, right)
        print("Left: " + str(left) + "; Right: " + str(right))
    elif nt.isConcentrating == False:
        print("Not concentrating")
        bot.drive(0,0)