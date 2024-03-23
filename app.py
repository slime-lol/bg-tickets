import os

os.system("pip install -r requirements.txt")

from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def hello():
  return "Hello BG Tickets!"

def run():
  app.run("127.0.0.1", port=8888)

def keep_alive():
  t = Thread(target=run)
  t.start()
