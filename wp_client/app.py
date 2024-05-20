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
print(targets)
interval = int(os.environ['INTERVAL'])

while True:
    for t in targets:
        try:
            resp = requests.get("http://" + t + "/wp-admin/setup-config.php")
            print("Issued GET to {}, received response code {}".format(t, resp.status_code))
        except:
            print("something bad happened, let's try again")
            continue
    time.sleep(interval)
