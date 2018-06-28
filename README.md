# Neuro-Gesture-Controlled-Robot
Controls small two-wheeled bot with Raspberry Pi using Myo armband and EMOTIV

## Libraries used :
*  [PyoConnect 1.0](http://www.fernandocosentino.net/pyoconnect/) - for using Myo armband with the Pi
*  [PyNetworkTables](https://github.com/robotpy/pynetworktables) - for using Network Tables with the Pi
*  [Adafruit BBIO 12C](https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/i2c) / [Adafruit Servo Library](https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library) - for driving motors with 16-Channel PWM Pi HAT

#### Notes :
* The Pi keeps a [static ip address](http://www.circuitbasics.com/how-to-set-up-a-static-ip-on-the-raspberry-pi/) as does the PC
* The PC and Pi connect to same private mobile hotspot
* The Pi runs the program "main.py" on [startup using .bashrc](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#bash)
