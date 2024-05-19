import mysql.connector
import os
import time

targets = os.environ['TARGETS']
targets = targets.split(" ")

interval = 3

while True:
    for t in targets:
        cnx = mysql.connector.connect(user='lab',password='lab123',host=t, database='lab_db')
        cnx.close()
    time.sleep(interval)