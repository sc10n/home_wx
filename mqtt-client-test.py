import paho.mqtt.client as mqtt

local_client = mqtt.Client()
local_client.connect("localhost")
local_client.loop_start()
local_client.publish("hello/world", "Hi there, I am a python MQTT client!")

raw_input("Hello sent, type enter to continue")