# This script is a simple PoC test for generating REST requests on an interval
# This will later be fleshed out with
# 1. Taking a config file as input which specifies
#   a. The endpoint(s) to hit
#   b. Request parameters (GET/POST/DELETE/UPDATE, payloads, etc)
#   c. The interval on which to send request (or a range in which to randomize)
# 2. Similar functionality for hitting other services

import requests
import time
import os
from paho.mqtt import client as mqtt_client
import random

targets = os.environ['TARGETS']
targets = targets.split(" ")
print(targets)
interval = int(os.environ['INTERVAL'])
mqtt_broker = os.environ['MQTT_SERVER']
hostname = os.environ['HOSTNAME']
port = 1883
topic = "web/{}".format(hostname)
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
    # For paho-mqtt 2.0.0, you need to add the properties parameter.
    # def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)

    # For paho-mqtt 2.0.0, you need to set callback_api_version.
    # client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(mqtt_broker, port)
    return client

def handle_mqtt_msg(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        handle_mqtt_msg(client, userdata, msg)

    client.subscribe(topic)
    client.on_message = on_message

client = connect_mqtt()
subscribe(client)

# while True:
#     for t in targets:
#         try:
#             resp = requests.get("http://" + t + "/employees")
#             print("Issued GET to {}, received response code {}".format(t, resp.status_code))
#         except:
#             print("something bad happened, let's try again")
#             continue
#     time.sleep(interval)
    
# Define some scenarios

