# Neuro-Gesture-Controlled-Robot
Controls small two-wheeled bot with PWM/Servo Pi HAT and Raspberry Pi 3 using Myo armband and EMOTIV EPOC

## Overview :
* Robot wheels move according to armband gyroscope axes
* EMOTIV overrides robot to force stop when user is not concentrating

## Libraries/SDKs/etc. used :
#### On the Rasp. Pi: 
*  [PyoConnect 1.0](http://www.fernandocosentino.net/pyoconnect/) - for using Myo armband with the Pi
*  [PyNetworkTables](https://github.com/robotpy/pynetworktables) - for using Network Tables with the Pi
*  [Adafruit PWM Servo Library](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/legacy) / [BBIO 12C](https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/i2c) - for driving motors with 16-Channel PWM Pi HAT
#### On the Local PC :
* [Emotiv SDK](https://github.com/Emotiv/community-sdk) - for using Emotiv EPOC information and using it
* [PyNetworkTables](https://github.com/robotpy/pynetworktables) - for the PC to send information to the Rasp. Pi

## Installing Libraries on Rasp. Pi:
#### PyoConnect :
Plug in bluetooth adapter for armband into Pi.
```
// permission to ttyACM0 - must restart linux user after this
sudo usermod -a -G dialout $USER

// dependencies
sudo apt-get install python-pip
sudo pip install pySerial --upgrade
sudo pip install enum34
sudo pip install PyUserInput
sudo apt-get install python-Xlib
sudo apt-get install python-tk
```
Now reboot.

Download and unzip PyoConnect 1.0 folder.
Then move files to folder with the code that will be used.

#### Pynetworktables :
```
sudo pip install pynetworktables
```
#### Servo PWM Library:
Install RPi.GPIO library.
```
sudo apt-get update
sudo apt-get install -y python3 python3-pip python-dev
sudo pip3 install rpi.gpio
```
Download the code (legacy branch, code used here)
```
git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/legacy
```
Use the files in Adafruit_PWM_Servo_Driver.

## Notes :
* The Pi keeps a [static ip address](http://www.circuitbasics.com/how-to-set-up-a-static-ip-on-the-raspberry-pi/) as does the PC
* The PC and Pi connect to same private mobile hotspot
* The Pi runs the program "[main.py](https://github.com/mkazazic2001/Neuro-Gesture-Controlled-Robot/tree/master/Rasp-Pi)" when [on startup using .bashrc](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#bash)
