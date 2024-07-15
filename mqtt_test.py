import requests
import time
import os
from paho.mqtt import client as mqtt_client
import random
import yaml
import json
from pprint import pprint
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-broker')
parser.add_argument('-client_id')
parser.add_argument('-config', 'tg_config.yml')
args=parser.parse_args()

broker = args.broker
port = 1883
config = args.config
client_id = args.client_id

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
            
    # For paho-mqtt 2.0.0, you need to set callback_api_version.
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, action):
    topic = f"{action['service_type']}/{action['service_host']}"
    print(f"Topic {topic}")
    msg = action['action']
    result = client.publish(topic,json.dumps(msg))
    print(result)
f = open(config, "r")
config = yaml.safe_load(f)
client = connect_mqtt()
client.loop_start()
for action in config['scenario']:
    print("running action")
    publish(client, action)
client.loop_stop()