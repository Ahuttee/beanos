from flask import Flask
from threading import Thread
import os
import requests
import time

app = Flask('Beanos')

@app.route('/')
def home():
    return "Hello world! :)"
def run():
  app.run(host='0.0.0.0',port=8080)

def ping():
  while True:
    url = os.environ["URL"]
    status = requests.get(url)
    print("Status", status)
    time.sleep(180)
  


def main():  
    server = Thread(target=run)
    pinger = Thread(target=ping)
    server.start()
    pinger.start()