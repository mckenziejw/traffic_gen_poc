#!/usr/bin/python3

import requests
import time
import os
from paho.mqtt import client as mqtt_client
import random
import multiprocessing
import json
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import signal
from pathlib import Path
import argparse
from scipy.stats import norm

parser = argparse.ArgumentParser()
parser.add_argument('-hostname', default='')
args = parser.parse_args()

config={}
with open('/etc/wifi_client/config.yml', 'r') as f:
    config = yaml.safe_load(f)

mqtt_broker = config['mqtt_broker']
hostname = args.hostname
traffic_gen_type = config['tgtype']
ss_count = config['ss_count']
port = config['port']

topic_1 = "{}/{}".format(traffic_gen_type, hostname)
topic_2 = "{}/{}".format('iot', hostname)
client_id = f'python-mqtt-{hostname}'
processes = []

def watch_youtube(path, watch_time=300):
    try:
        chrome_options = Options()
        service = Service(executable_path='/usr/bin/chromedriver')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location="/usr/bin/google-chrome-stable"
        browser = webdriver.Chrome(options=chrome_options, service=service)
        browser.get(path)
        for i in range(10):
            time.sleep(1)
        video = browser.find_element(By.CSS_SELECTOR,'.ytp-large-play-button')
        video.click() #hits space
        #time.sleep(10)
        current_time = time.time()
        end_time = time.time() + watch_time
        i = 1
        while current_time <= end_time:
            if i <= ss_count:
                browser.get_screenshot_as_file(f"/root/test-ss-{i}.png")
            time.sleep(60)
            i = i + 1
        browser.quit()
    except Exception as e:
        print(e)
        pass

def watch_twitch(path, watch_time=300):
    try:
        chrome_options = Options()
        service = Service(executable_path='/usr/bin/chromedriver')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location="/usr/bin/google-chrome-stable"
        browser = webdriver.Chrome(options=chrome_options, service=service)
        browser.get(path)
        for i in range(10):
            time.sleep(1)
        #video = browser.find_element(By.CSS_SELECTOR,'.ytp-large-play-button')
        #video.click() #hits space
        #time.sleep(10)
        current_time = time.time()
        end_time = time.time() + watch_time
        i = 1
        while current_time <= end_time:
            if i <= ss_count:
                browser.get_screenshot_as_file(f"/root/twitch-ss-{i}.png")
            time.sleep(60)
            i = i + 1
        browser.quit()
    except Exception as e:
        print(e)
        pass
    
def gdrive_download(path, watch_time=300):
    try:
        chrome_options = Options()
        service = Service(executable_path='/usr/bin/chromedriver')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location="/usr/bin/google-chrome-stable"
        browser = webdriver.Chrome(options=chrome_options, service=service)
        browser.get(path)
        time.sleep(watch_time)
        browser.quit()
    except Exception as e:
        print(e)
        pass

def kill_all_loops(processes):
    for p in processes:
        p.kill()
    processes = []

def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(topic_1)
            client.subscribe(topic_2)
        else:
            print("Failed to connect, return code %d\n", rc)

def do_action(action):
    if action['type'] == 'get':
        if action['loop_for'] == 0:
            while True:
                for t in action['targets']:
                    try:
                        resp = requests.get("{}/{}".format(t, action['uri']))
                        print(f"GET response from {t} with status: {resp.status_code}")
                    except Exception as e:
                        print(e)
                        pass
                if action.get('loop_delay'):
                    delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                    time.sleep(delay)
        elif action['loop_for'] == 1:
            for t in action['targets']:
                try:
                    resp = requests.get("{}/{}".format(t, action['uri']))
                    print(f"GET response from {t} with status: {resp.status_code}")
                except Exception as e:
                    print(e)
                    pass
            if action.get('loop_delay'):
                delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                time.sleep(delay)
        elif action['loop_for'] >1:
            for _ in range(action['loop_for']):
                for t in action['targets']:
                    try:
                        resp = requests.get("{}/{}".format(t, action['uri']))
                        print(f"GET response from {t} with status: {resp.status_code}")
                    except Exception as e:
                        print(e)
                        pass
                if action.get('loop_delay'):
                    delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                    time.sleep(delay)
    elif action['type'] == 'post':
        ## do a post
        if action['loop_for'] == 0:
            while True:
                for t in action['targets']:
                    try:
                        resp = requests.post("http://{}/{}".format(t, action['uri']), data = json.dumps(action['payload']))
                        print(f"GET response from {t} with status: {resp.status_code}")
                    except Exception as e:
                        print(e)
                        pass
                if action.get('loop_delay'):
                    delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                    time.sleep(delay)
        elif action['loop_for'] == 1:
            for t in action['targets']:
                try:
                    resp = requests.post("{}/{}".format(t, action['uri']), data = json.dumps(action['payload']))
                    print(f"GET response from {t} with status: {resp.status_code}")
                except Exception as e:
                    print(e)
                    pass
            if action.get('loop_delay'):
                delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                time.sleep(delay)
        elif action['loop_for'] >1:
            for _ in range(action['loop_for']):
                for t in action['targets']:
                    try:
                        resp = requests.post("{}/{}".format(t, action['uri']), data = json.dumps(action['payload']))
                        print(f"GET response from {t} with status: {resp.status_code}")
                    except Exception as e:
                        print(e)
                        pass
                if action.get('loop_delay'):
                    delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                    time.sleep(delay)
    elif action['type'] == 'watch_youtube':
        for t in action['targets']:
            try:
                delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                watch_youtube(f"https://youtube.com/watch?v={t}", delay)
            except Exception as e:
                print(e)
                pass
    elif action['type'] == 'watch_twitch':
        for t in action['targets']:
            try:
                delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                watch_twitch(f"https://twitch.tv/{t}", delay)
            except Exception as e:
                print(e)
                pass
    elif action['type'] == 'gdrive_download':
        if action['loop_for'] == 0:
            while True:
                for t in action['targets']:
                    try:
                        delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                        gdrive_download(f"https://drive.google.com/{t}", delay)
                    except Exception as e:
                        print(e)
                        pass
        elif action['loop_for'] == 1:
            for t in action['targets']:
                try:
                    delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                    gdrive_download(f"https://drive.google.com/{t}", delay)
                except Exception as e:
                    print(e)
                    pass
        elif action['loop_for'] > 1:
            for _ in range(action['loop_for']):
                for t in action['targets']:
                    try:
                        delay = random.randint(action['loop_delay']['min'],action['loop_delay']['max'])
                        gdrive_download(f"https://drive.google.com/{t}", delay)
                    except Exception as e:
                        print(e)
                        pass
    elif action['type'] == 'iot_telemetry':
        # Process parameters
        delta = 0.25
        dt = 0.1
        def on_pub(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
            try:
                userdata.remove(mid)
            except KeyError:
                print("on_publish() is called with a mid not present in unacked_publish")
                print("This is due to an unavoidable race-condition:")
                print("* publish() return the mid of the message sent.")
                print("* mid from publish() is added to unacked_publish by the main thread")
                print("* on_publish() is called by the loop_start thread")
                print("While unlikely (because on_publish() will be called after a network round-trip),")
                print(" this is a race-condition that COULD happen")
                print("")
                print("The best solution to avoid race-condition is using the msg_info from publish()")
                print("We could also try using a list of acknowledged mid rather than removing from pending list,")
                print("but remember that mid could be re-used !")
        mqttc = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
        mqttc.on_publish = on_pub
        mqttc.connect("192.168.10.143", port=1883, keepalive=120, bind_address="")
        # Initial condition.
        x = 0.0
        
        while True:
            try:
                x = x + norm.rvs(scale=delta**2*dt)
                mqttc.publish("{'time':{}, 'frequency':{}}".format(time.now(), x))
                time.sleep(2)
            except Exception as e:
                print(e)
                pass

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

