from flask import Flask
from threading import Thread

app = Flask("beanos")

@app.route("/")
def index():
  return "Hello world :)"

def run():
  app.run(host="0.0.0.0", port=8080)

def main():
  t = Thread(target=run)
  t.start()