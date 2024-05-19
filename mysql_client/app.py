from MySQLdb import _mysql
import os
import time

targets = os.environ['TARGETS']
targets = targets.split(" ")

interval = 3

while True:
    for t in targets:
        try:
            cnx = _mysql.connect(
                user='lab',
                password='lab123',
                host=t,
                database="lab_db"
                )
            cnx.close()
        except:
            print("Something bad happened, let's try again")
    time.sleep(interval)