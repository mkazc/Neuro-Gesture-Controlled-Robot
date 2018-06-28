import sys
import os
import platform
import time
import ctypes
import pygame

import msvcrt
from ctypes import *

libEDK = CDLL(r"C:\Users\rebec\OneDrive\Documents\NASA\Community SDK\community-sdk-master\bin\win64\edk.dll")

IEE_EmoEngineEventCreate = libEDK.IEE_EmoEngineEventCreate
IEE_EmoEngineEventCreate.restype = c_void_p
eEvent = IEE_EmoEngineEventCreate()

IEE_EmoEngineEventGetEmoState = libEDK.IEE_EmoEngineEventGetEmoState
IEE_EmoEngineEventGetEmoState.argtypes = [c_void_p, c_void_p]
IEE_EmoEngineEventGetEmoState.restype = c_int

IS_GetTimeFromStart = libEDK.IS_GetTimeFromStart
IS_GetTimeFromStart.argtypes = [ctypes.c_void_p]
IS_GetTimeFromStart.restype = c_float

IEE_EmoStateCreate = libEDK.IEE_EmoStateCreate
IEE_EmoStateCreate.restype = c_void_p
eState = IEE_EmoStateCreate()

# interest
IS_PerformanceMetricGetInterestModelParams = libEDK.IS_PerformanceMetricGetInterestModelParams
IS_PerformanceMetricGetInterestModelParams.restype = c_void_p
IS_PerformanceMetricGetInterestModelParams.argtypes = [c_void_p]

IS_PerformanceMetricGetInterestScore = libEDK.IS_PerformanceMetricGetInterestScore
IS_PerformanceMetricGetInterestScore.restype = c_float
IS_PerformanceMetricGetInterestScore.argtypes = [c_void_p]

# engagement
IS_PerformanceMetricGetEngagementBoredomModelParams = libEDK.IS_PerformanceMetricGetEngagementBoredomModelParams
IS_PerformanceMetricGetEngagementBoredomModelParams.restype = c_void_p
IS_PerformanceMetricGetEngagementBoredomModelParams.argtypes = [c_void_p]

IS_PerformanceMetricGetEngagementBoredomScore = libEDK.IS_PerformanceMetricGetEngagementBoredomScore
IS_PerformanceMetricGetEngagementBoredomScore.restype = c_float
IS_PerformanceMetricGetEngagementBoredomScore.argtypes = [c_void_p]

# stress
IS_PerformanceMetricGetStressModelParams = libEDK.IS_PerformanceMetricGetStressModelParams
IS_PerformanceMetricGetStressModelParams.restype = c_void_p
IS_PerformanceMetricGetStressModelParams.argtypes = [c_void_p]

IS_PerformanceMetricGetStressScore = libEDK.IS_PerformanceMetricGetStressScore
IS_PerformanceMetricGetStressScore.restype = c_float
IS_PerformanceMetricGetStressScore.argtypes = [c_void_p]

# -------------------------------------------------------------------------

def logPerformanceMetrics(eState):

    #print >> f, getInterest(eState)
    #print >> f, getEngagement(eState)
    print >> f, getStress(eState)
    print >> f, isConcentrating(eState)
    f.flush()

    print >> f, '\n'

def getInterest(eState):
    return IS_PerformanceMetricGetInterestScore(eState)

def getEngagement(eState):
    return IS_PerformanceMetricGetEngagementBoredomScore(eState)

def getStress(eState):
    return IS_PerformanceMetricGetStressScore(eState)

def isConcentrating(eState):
    return getStress(eState) > 0.5
    #return getInterest(eState) > 0.5
    #return getEngagement(eState) > 0.7

def kbhit():
    return msvcrt.kbhit()


# -------------------------------------------------------------------------

userID = c_uint(0)
user = pointer(userID)
option = c_int(0)
state = c_int(0)
composerPort = c_uint(1726)
timestamp = c_float(0.0)

PM_EXCITEMENT = 0x0001,
PM_RELAXATION = 0x0002,
PM_STRESS = 0x0004,
PM_ENGAGEMENT = 0x0008,

PM_INTEREST = 0x0010,
PM_FOCUS = 0x0020

if libEDK.IEE_EngineConnect("Emotiv Systems-5") != 0:
    print ("Emotiv Engine start up failed.")

print ("Start receiving Emostate! Press any key to stop logging...\n")
#f = file('PerfomanceMetrics.csv', 'w')
f = open('PerfomanceMetrics.csv', 'w')

from networktables import NetworkTables
import logging
logging.basicConfig(level=logging.DEBUG)
NetworkTables.initialize()

table = NetworkTables.getTable("concentration")

# blank = False;
#
# while 1:
#
#     blank = not blank
#
#     if kbhit():
#         break
#
#     state = libEDK.IEE_EngineGetNextEvent(eEvent)
#     if state == 0:
#         eventType = libEDK.IEE_EmoEngineEventGetType(eEvent)
#         libEDK.IEE_EmoEngineEventGetUserId(eEvent, user)
#         if eventType == 64:  # libEDK.IEE_Event_enum.IEE_EmoStateUpdated
#             libEDK.IEE_EmoEngineEventGetEmoState(eEvent, eState)
#             logPerformanceMetrics(eState)
#             table.putBoolean("isConcentrating", isConcentrating(eState))
#             #table.putBoolean("isConcentrating", blank)
#     elif state != 0x0600:
#         print
#         "Internal error in Emotiv Engine ! "
#     time.sleep(0.1)
# -------------------------------------------------------------------------
# f.close()
# libEDK.IEE_EngineDisconnect()
# libEDK.IEE_EmoStateFree(eState)
# libEDK.IEE_EmoEngineEventFree(eEvent)


# -------------------------------------------------------------------------

pygame.init()
pygame.display.set_mode((500,500))

blank = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # sys.exit() if sys is imported
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                blank = not blank

    print (blank)
    table.putBoolean("isConcentrating", blank)