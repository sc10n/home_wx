import time
import grovepi
import paho.mqtt.client as mqtt
import json

# Define LED pins
BLUE_LED = 2
RED_LED = 3
GREEN_LED = 5

# Set the LED pins to output mode
grovepi.pinMode(RED_LED, "OUTPUT")
grovepi.pinMode(GREEN_LED, "OUTPUT")
grovepi.pinMode(BLUE_LED, "OUTPUT")
#time.sleep(1) # give the hardware time to initialize



def led_value_check(payload, color):
    # type: (object, object) -> object
    # validate led values
    # payload must contain color
    # payload[color] must be an int between 0-255
    if color in payload and isinstance(payload[color], int) and 0 <= payload[color] <= 255:
        print str(payload[color]) + " is not null and within range"
        return True
    else:
        print "Looking for color " + color + " " + str(payload) + " nothing found"
        return False

def on_connect(client, userdata, flags, rc):
    """Called each time the client connects to the message broker
    :param client: The client object making the connection
    :param userdata: Arbitrary context specified by the user program
    :param flags: Response flags sent by the message broker
    :param rc: the connection result
    :return: None
    """
    # subscribe to the LEDs topic when connected
    client.subscribe("SNHU/IT697/leds")

def on_message(client, userdata, msg):
    """Called for each message received
    :param client: The client object making the connection
    :param userdata: Arbitrary context specified by the user program
    :param msg: The message from the MQTT broker
    :return: None
    """
    print(msg.topic, msg.payload)
    payload = json.loads(msg.payload)
    # the legal values for analogWrite are 0 - 255
    if led_value_check(payload, 'red'):
        grovepi.analogWrite(RED_LED, payload['red'])
    if led_value_check(payload, 'green'):
        grovepi.analogWrite(GREEN_LED, payload['green'])
    if led_value_check(payload, 'blue'):
        grovepi.analogWrite(BLUE_LED, payload['blue'])

local_client = mqtt.Client()
local_client.on_connect = on_connect
local_client.on_message = on_message

local_client.connect("localhost")
local_client.loop_forever()