import sys
import time
import os
from networktables import NetworkTables

# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.DEBUG)

ledPath = "/home/pi/LED_Matrix/led-screens/"
isConcentrating = False

ip = ''
print('Initializing NetworkTables')
NetworkTables.initialize(server=ip)

def valueChanged(table, key, value, isNew):
    global isConcentrating
    print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))
    sys.stdout.flush()
    isConcentrating = led.getBoolean("isConcentrating", False)

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)


NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

led = NetworkTables.getTable("concentration")
led.addEntryListener(valueChanged)

   