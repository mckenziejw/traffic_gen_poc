from ftplib import FTP
import os
import time

interval = int(os.environ['INTERVAL'])
targets = os.environ['TARGETS']
print(targets)
targets = targets.split(" ")

while True:
    for t in targets:
        try:
            with FTP(host=t, user='lab', passwd='Juniper123') as ftp:
                print(ftp.getwelcome())
        except:
            print("Something bad happened, let's try again")
            continue
    time.sleep(interval)
    