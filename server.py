import flask
from flask import Flask
import threading
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  while True:
    return f"trolley"

def run():
  from waitress import serve
  serve(app, host="0.0.0.0", port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
  return