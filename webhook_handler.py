from flask import Flask
import subprocess
import requests
from pymongo import MongoClient

client = MongoClient("mongodb://147.182.251.133")
db = client['psks']
app = Flask(__name__)

@app.route("/update_psks", methods=['POST'])
def update_psks():
    data = request.get_json()
    db.insert_one(data)
    print(data)


if __name__ == "__main__":
    app.run(ssl_context='adhoc', host='0.0.0.0', port=80)