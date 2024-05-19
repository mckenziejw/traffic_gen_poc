# This script is a simple PoC test for generating REST requests on an interval
# This will later be fleshed out with
# 1. Taking a config file as input which specifies
#   a. The endpoint(s) to hit
#   b. Request parameters (GET/POST/DELETE/UPDATE, payloads, etc)
#   c. The interval on which to send request (or a range in which to randomize)
# 2. Similar functionality for hitting other services

import requests
import time

api_endpoint = 'http://172.18.0.2'
port = 80
interval = 3 #(in seconds)

while True:
    resp = requests.get(api_endpoint)
    print("Issued GET to {}, received response code {}".format(api_endpoint, resp.status_code))
    time.sleep(interval)
