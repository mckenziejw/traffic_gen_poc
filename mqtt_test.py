import requests
import time
import os
from paho.mqtt import client as mqtt_client
import random

broker = '10.41.0.7'
port = 1883
topic = 'web/web-client-1'
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
    client.connect(broker, port)
    return client

def publish(client):
    msg_count = 1
    msg = {'action':'go'}
    result = client.publish(topic,msg)
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

client = connect_mqtt()
publish(client)