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
import multiprocessing
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

mqtt_broker = os.environ['MQTT_SERVER']
hostname = os.environ['HOSTNAME']
traffic_gen_type = os.environ['TGTYPE']
port = 1883
topic = "{}/{}".format(traffic_gen_type, hostname)
client_id = f'python-mqtt-{random.randint(0, 1000)}'
processes = []

def watch_youtube(path, watch_time=300):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(path)
    for i in range(10):
        time.sleep(1)
    video = browser.find_element(By.ID,'movie_player')
    video.send_keys(Keys.SPACE) #hits space
    time.sleep(watch_time)
    browser.quit()

def kill_all_loops(processes):
    for p in processes:
        p.kill()
    processes = []

def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(topic)
        else:
            print("Failed to connect, return code %d\n", rc)

def do_action(action):
    if action['type'] == 'get':
        if action['loop_for'] == 0:
            while True:
                for t in action['targets']:
                    resp = requests.get("{}/{}".format(t, action['uri']))
                    print(f"GET response from {t} with status: {resp.status_code}")
                if action.get('loop_delay'):
                    delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                    time.sleep(delay)
        elif action['loop_for'] == 1:
            for t in action['targets']:
                resp = requests.get("{}/{}".format(t, action['uri']))
                print(f"GET response from {t} with status: {resp.status_code}")
            if action.get('loop_delay'):
                delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                time.sleep(delay)
        elif action['loop_for'] >1:
            for _ in range(action['loop_for']):
                for t in action['targets']:
                    resp = requests.get("{}/{}".format(t, action['uri']))
                    print(f"GET response from {t} with status: {resp.status_code}")
                if action.get('loop_delay'):
                    delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                    time.sleep(delay)
    elif action['type'] == 'post':
        ## do a post
        if action['loop_for'] == 0:
            while True:
                for t in action['targets']:
                    resp = requests.post("http://{}/{}".format(t, action['uri']), data = json.dumps(action['payload']))
                    print(f"GET response from {t} with status: {resp.status_code}")
                if action.get('loop_delay'):
                    delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                    time.sleep(delay)
        elif action['loop_for'] == 1:
            for t in action['targets']:
                resp = requests.post("{}/{}".format(t, action['uri']), data = json.dumps(action['payload']))
                print(f"GET response from {t} with status: {resp.status_code}")
            if action.get('loop_delay'):
                delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                time.sleep(delay)
        elif action['loop_for'] >1:
            for _ in range(action['loop_for']):
                for t in action['targets']:
                    resp = requests.post("{}/{}".format(t, action['uri']), data = json.dumps(action['payload']))
                    print(f"GET response from {t} with status: {resp.status_code}")
                if action.get('loop_delay'):
                    delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                    time.sleep(delay)
    elif action['type'] == 'watch_youtube':
        for t in action['targets']:
            delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
            watch_youtube(f"https://youtube.com/watch?v={t}", delay)
    # elif action['type'] == 'put':
    #     ## do a put
    #     if action['loop_for'] == 0:
    #         while True:
    #             for t in action['targets']:
    #                 resp = requests.put("{}/{}".format(t, action['uri']))
    #                 print(f"GET response from {t} with status: {resp.status_code}")
    #             if action.get('loop_delay'):
    #                 delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
    #                 time.sleep(delay)
    #     elif action['loop_for'] == 1:
    #         for t in action['targets']:
    #             resp = requests.put("{}/{}".format(t, action['uri']))
    #             print(f"GET response from {t} with status: {resp.status_code}")
    #         if action.get('loop_delay'):
    #             delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
    #             time.sleep(delay)
    #     elif action['loop_for'] >1:
    #         for _ in range(action['loop_for']):
    #             for t in action['targets']:
    #                 resp = requests.put("{}/{}".format(t, action['uri']))
    #                 print(f"GET response from {t} with status: {resp.status_code}")
    #             if action.get('loop_delay'):
    #                 delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
    #                 time.sleep(delay)
    # elif action['type'] == 'delete':
    #     if action['loop_for'] == 0:
    #         while True:
    #             for t in action['targets']:
    #                 resp = requests.delete("{}/{}".format(t, action['uri']))
    #                 print(f"GET response from {t} with status: {resp.status_code}")
    #             if action.get('loop_delay'):
    #                 delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
    #                 time.sleep(delay)
    #     elif action['loop_for'] == 1:
    #         for t in action['targets']:
    #             resp = requests.delete("{}/{}".format(t, action['uri']))
    #             print(f"GET response from {t} with status: {resp.status_code}")
    #         if action.get('loop_delay'):
    #             delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
    #             time.sleep(delay)
    #     elif action['loop_for'] >1:
    #         for _ in range(action['loop_for']):
    #             for t in action['targets']:
    #                 resp = requests.delete("{}/{}".format(t, action['uri']))
    #                 print(f"GET response from {t} with status: {resp.status_code}")
    #             if action.get('loop_delay'):
    #                 delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
    #                 time.sleep(delay)

def handle_mqtt_msg(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    action = json.loads(msg.payload.decode())
    if action['type'] == 'kill':
        kill_all_loops(processes)
    else:
        req_type = action['type']
        targets = action['targets']
        loop_for = action['loop_for']
        if action['create_thread']:
            p = multiprocessing.Process(target=do_action, args=[action])
            processes.append(p)
            p.start()
            print(f"Created long-running process {p.pid}")
            print(processes)
        else:
            print("running a one-off request")
            print(action)
            do_action(action)    
    
    
def on_message(client, userdata, msg):
        handle_mqtt_msg(client, userdata, msg)
        
        
client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, port)
client.loop_forever()

