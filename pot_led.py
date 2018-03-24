# Grove pi test with Pot and LED
import smbus
import time
import grovepi

# for RPI version 1, use "bus = smbus.SMBus(0)"
#bus = smbus.SMBus(0)

# This is the address we setup in the Arduino Program
#address = 0x04
pot = 2
led = 5
grovepi.pinMode(led, "OUTPUT")
time.sleep(1)
i = 0
while True:
    try:
        i = grovepi.analogRead(pot)
        print i
        grovepi.analogWrite(led, i//4)
    except IOError:
        print "Error"