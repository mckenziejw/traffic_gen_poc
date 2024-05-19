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

targets = os.environ['TARGETS']
targets = targets.split(" ")

interval = 3 #(in seconds)

while True:
    for t in targets:
        resp = requests.get('http://' + t)
        print("Issued GET to {}, received response code {}".format(api_endpoint, resp.status_code))
    time.sleep(interval)
