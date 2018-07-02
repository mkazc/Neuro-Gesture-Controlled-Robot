#!/usr/bin/python
from PyoConnect import *
myo = Myo(sys.argv[1] if len(sys.argv) >= 2 else None)
from time import sleep
from abc import ABCMeta, abstractmethod

HIGH_STARTL = 360
MID_HIGH_STARTL = 329
MID_LOW_STARTL = 316
LOW_STARTL = 294
    
HIGH_STARTR = 290
MID_HIGH_STARTR = 321
MID_LOW_STARTR = 335
LOW_STARTR = 360


#used to find the motor speed value to the given myo value
def linear(self, myo_high, myo_low, speed_high, speed_low):
    my_speed = speed_high - speed_low
    mx_myo = myo_high - myo_low
    if mx_myo == 0:
        return 0
    else:
        m = my_speed/mx_myo
        change_myo = self - myo_low
        change_speed = m * change_myo
        linear = change_speed + speed_low
        return int(linear)

#used to average pitch and yaw motor speed values
#n is number of a variable
def avg(pitch_speed, value_pitch, yaw_speed, value_yaw):
    all_pitch = pitch_speed * value_pitch
    all_yaw = yaw_speed * value_yaw
    both_speed = all_pitch + all_yaw
    values = value_pitch + value_yaw
    if values == 0:
        return 0
    else:
        avg = both_speed/values
        return int(avg)


Rolling = False
direction = 1

class Myoband(object):
    def ___init___(self):
        self.myo = myo()
    def initialize(self):
        myo.connect()
        myo.rotSetCenter()
        myo.getPitch()
        myo.getYaw()
        myo.getRoll()
    def start(self):
        myo.run()
        myo.tick()
    def motor_speeds(self):
        pitch, yaw, roll = myo.rotPitch(), myo.rotYaw(), myo.rotRoll()
        left, right = self.orientation_to_motor_speeds(pitch, yaw, roll)
        return left, right
    def orientation_to_motor_speeds(self, pitch, yaw, roll):
        left, right = getSpeed(pitch, yaw, roll)
        return left, right


class Orientation_Speeds(object):
    __metaclass__ = ABCMeta
    #Changing axis list for myo values
    axis_list = []
    #ls list is left motor speed values
    ls_list = []
    #rs list is right motor speed values
    rs_list = []
    def getValues(self, value):
        self.value = value
        axis_list = self.axis_list
        if value > self.axis_list[0]:
            left = self.ls_list[0]
            right = self.rs_list[0]
            n = 1
        elif self.axis_list[0] > value > self.axis_list[1]:
            left = linear(value, self.axis_list[0], self.axis_list[1], self.ls_list[0], self.ls_list[1])
            right = linear(value, self.axis_list[0], self.axis_list[1], self.rs_list[0], self.rs_list[1])
            n = 1
        elif self.axis_list[1] > value > self.axis_list[2]:
            left = self.ls_list[1]
            right = self.rs_list[1]
            n = 0
        elif self.axis_list[2] > value > self.axis_list[3]:
            left = linear(value, self.axis_list[2], self.axis_list[3], self.ls_list[2], self.ls_list[3])
            right = linear(value, self.axis_list[2], self.axis_list[3], self.rs_list[2], self.rs_list[3])
            n = 1
        elif self.axis_list[3] > value:
            left = self.ls_list[3]
            right = self.rs_list[3]
            n = 1
        else:
            left = self.ls_list[2]
            right = self.rs_list[2]
            n = 0
        return left, right, n
    
    @abstractmethod
    def axis_type(self):
        """"Returns axis type string"""
        pass


class Pitch(Orientation_Speeds):
    #The pitch axis list goes from pointing downward to upward
    axis_list = [0.5, 0.2, -0.2, -0.5]
    ls_list = [LOW_STARTL, MID_LOW_STARTL, MID_HIGH_STARTL, HIGH_STARTL]
    rs_list = [LOW_STARTR, MID_LOW_STARTR, MID_HIGH_STARTR, HIGH_STARTR]
    
    def getDirection(self, p):
        self.p = p
        if self.p < self.axis_list[2]:
            direction = 1
            return direction
        elif self.p > self.axis_list [1]:
            direction = -1
            return direction
    
    def axis_type(self):
        """"Returning axis type string it represents."""
        return 'pitch'
pitch = Pitch()


class Forward_Yaw(Orientation_Speeds):
    #The Yaw axis list goes from pointing right to left
    axis_list = [0.6, 0.2, -0.2, -0.6]
    ls_list = [HIGH_STARTL, MID_HIGH_STARTL, MID_HIGH_STARTL, MID_HIGH_STARTL]
    rs_list = [MID_HIGH_STARTR, MID_HIGH_STARTR, MID_HIGH_STARTR, HIGH_STARTR]
    def axis_type(self):
        """"Returning axis type string it represents."""
        return 'forwardyaw'
fyaw = Forward_Yaw()

class Backward_Yaw(Orientation_Speeds):
    #The Yaw axis list goes from pointing right to left
    axis_list = [0.6, 0.2, -0.2, -0.6]
    ls_list = [LOW_STARTL, MID_LOW_STARTL, MID_LOW_STARTL, MID_LOW_STARTL]
    rs_list = [MID_LOW_STARTR, MID_LOW_STARTR, MID_LOW_STARTR, LOW_STARTR]
    def axis_type(self):
        """"Returning axis type string it represents."""
        return 'backwardyaw'
byaw = Backward_Yaw()

class Roll(Orientation_Speeds):
    #The roll axis list goes from twisting arm left to right
    axis_list = [0.8, 0.2, -0.2, -0.7]
    ls_list = [LOW_STARTL, MID_LOW_STARTL, MID_HIGH_STARTL, HIGH_STARTL]
    rs_list = [HIGH_STARTR, MID_HIGH_STARTR, MID_LOW_STARTR, LOW_STARTR]
    def getRolling(self, r):
        self.r = r
        if self.axis_list[1] > self.r > self.axis_list[2]:
            Rolling = False
        else:
            Rolling = True
        return Rolling
    def axis_type(self):
        """"Returning axis type string it represents."""
        return 'roll'
roll = Roll()

def getSpeed(p,y,r):
    p_left, p_right, pn = pitch.getValues(p)
    direction = 1
    y_left, y_right, yn = fyaw.getValues(y)
    direction = pitch.getDirection(p)
    if direction == 1:
        y_left, y_right, yn = fyaw.getValues(y)
    elif direction == -1:
        y_left, y_right, yn = byaw.getValues(y)
    _,_,isRolling = roll.getValues(r)
    if isRolling == 1:
        left, right, _ = roll.getValues(r)
    elif isRolling == 0:
        left = avg(p_left, pn, y_left, yn)
        right = avg(p_right, pn, y_right, yn)
    return left, right


def onPoseEdge(pose, edge):
    if (pose == 'doubleTap') or (pose == 'fist') and (edge == "on"):
        myo.rotSetCenter()
        myo.getPitch()
        myo.getYaw()
        myo.getRoll()
        
def onPeriodic():
    myo.getPitch()
    if myo.isLocked():
        myo.unlock("hold")


myo.onPoseEdge = onPoseEdge
myo.onPeriodic = onPeriodic
    
