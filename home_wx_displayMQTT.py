# Home_Weather_DisplayMQTT.py
#
# This is an project for using the Grove RGB LCD Display and the Grove DHT Sensor from the GrovePi starter kit
#
# In this project, the Temperature and humidity from the DHT sensor is printed on the RGB-LCD Display
#
#
# Note the dht_sensor_type below may need to be changed depending on which DHT sensor you have:
#  0 - DHT11 - blue one - comes with the GrovePi+ Starter Kit
#  1 - DHT22 - white one, aka DHT Pro or AM2302
#  2 - DHT21 - black one, aka AM2301
#
# For more info please see: http://www.dexterindustries.com/topic/537-6c-displayed-in-home-weather-project/
#
'''
The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan
import paho.mqtt.client as mqtt
import time
import json
import logging

dht_sensor_port = 7 # connect the DHt sensor to port 7
dht_sensor_type = 0 # use 0 for the blue-colored sensor and 1 for the white-colored sensor
local_time = int(time.time()) # grabbing timestamp and converting to int
mosquitto_org_topic = "SNHU/IT697/james_thompson_snhu_edu/sensor/data/json" #MQTT Topic
test_mosquitto_host = "test.mosquitto.org" #Remote test broker
local_mqtt_host = "localhost" # No place like home

# set green as backlight color
# we need to do it just once
setRGB(0,255,0)
# Variables for temperature thresholds.
warmF = 74.0
justRightF = 72.0
coolF = 73.0

# Function to convert Celsius to Fahrenheit
def celToFahr(temp):
        tempf = float((temp * 9 / 5 ) + 32 )
        return tempf

# Function to build the json data to publish
def buildJson(tempf, hum):
    data = {
        'timestamp': local_time,
        'data': {
            'temperature': tempf,
            'humidity': hum
        }
    }
    data_json = json.dumps(data)
    return data_json

# Function to connect publish to the MQTT broker (needs the hostname, temp and humidity inputs)
def publishMQTT(host, tempf, hum):
    local_client = mqtt.Client()
    local_client.connect(host)
    local_client.publish(mosquitto_org_topic, buildJson(tempf, hum))

while True:
        try:
        # get the temperature and Humidity from the DHT sensor
                [ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)

                tempf = celToFahr(temp)

                # Change the screen colors
                if tempf >= warmF:
                    logging.warning('I am warm')
                    setRGB(255, 0, 0)
                elif tempf <= coolF:
                    logging.warning("I am cool")
                    setRGB(0, 0, 255)
                elif tempf == justRightF:
                    logging.warning('I am just right')
                    setRGB(0, 255, 0)
                # check if we have nans
                # if so, then raise a type error exception
                if isnan(temp) is True or isnan(hum) is True:
                        raise TypeError('nan error')

                print("temp =", tempf, "F\thumidity =", hum,"%")



                t = str(tempf)
                h = str(hum)

                # MQTT Publish to remote
                publishMQTT(test_mosquitto_host,tempf,hum)
                # MQTT Publish to local
                publishMQTT(local_mqtt_host, tempf, hum)
                # wait some time before re-updating the LCD
                sleep(5.00)

        # instead of inserting a bunch of whitespace, we can just insert a \n
        # we're ensuring that if we get some strange strings on one line, the 2nd one won't be affected
                setText_norefresh("Temp:" + t + "F\n" + "Humidity :" + h + "%")

                sleep(1)

        except (IOError, TypeError) as e:
                print(str(e))
                # and since we got a type error
                # then reset the LCD's text
                setText("")
                sleep(0.05)

        except KeyboardInterrupt as e:
                print(str(e))
                # since we're exiting the program
                # it's better to leave the LCD with a blank text
                setText("")
                setRGB(0,0,0)
                break



