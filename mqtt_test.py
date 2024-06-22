import requests
import time
import os
from paho.mqtt import client as mqtt_client
import random
import yaml
import json
from pprint import pprint

broker = '10.41.0.7'
port = 1883
client_id = f'python-mqtt-1'

def connect_mqtt():
    #def on_connect(client, userdata, flags, rc):
    # For paho-mqtt 2.0.0, you need to add the properties parameter.
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    #client = mqtt_client.Client(client_id)

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
    result = client.publish(topic,json.dumps(msg))
    result = client.publish(topic,json.dumps(msg))
    print(result)
    # while True:
    #      time.sleep(1)
    #      msg = f"messages: {msg_count}"
    #      result = client.publish(topic, msg)
    #      # result: [0, 1]
    #      status = result[0]
    #      if status == 0:
    #          print(f"Send `{msg}` to topic `{topic}`")
    #      else:
    #          print(f"Failed to send message to topic {topic}")
    #      msg_count += 1
    #      if msg_count > 5:
    #          break
f = open("tg_config.yml", "r")
config = yaml.safe_load(f)
client = connect_mqtt()
pprint(config)
client.loop_start()
for action in config['scenario']:
    print("running action")
    publish(client, action)
client.loop_stop()