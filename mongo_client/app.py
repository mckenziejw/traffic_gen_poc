from pymongo import MongoClient
import os
import time

targets = os.environ['TARGETS']
targets = targets.split(" ")
print(targets)
interval = int(os.environ['INTERVAL'])

while True:
    for t in targets:
        try:
            client = MongoClient(t)
            client.admin.command('ping')
            client.close()
        except:
            print("Something bad happened, let's try again")
    time.sleep(interval)
