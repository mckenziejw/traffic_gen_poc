from ftplib import FTP
import os
import time

interval = 3
targets = os.environ['TARGETS']
targets = targets.split(" ")

while True:
    for t in targets:
        with FTP(host=t, user='lab', passwd='Juniper123') as ftp:
            print(ftp.getwelcome())
    time.sleep(interval)
    