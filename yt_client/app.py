from pytube import YouTube
import os
import time
videos = [
    '81nWjP6nhGc',
    'BPZmnn0Yh8Y',
    'NkRIoD2qBzE'
]

targets = os.environ['TARGETS']
targets = targets.split(" ")
print(targets)
interval = int(os.environ['INTERVAL'])

def download_callback(strm, fpath):
    os.remove(fpath)

while True:
    for t in targets:
        try:
            yt = YouTube('http://youtube.com/watch?'+t, on_complete_callback=download_callback)
        except:
            print("Something bad happened, let's try again")
    time.sleep(interval)
