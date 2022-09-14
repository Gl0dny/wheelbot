#!/usr/bin/python3
from re import template
import time
from multiprocessing import Process, Queue
from flask import Flask, render_template, Response

app = Flask(__name__)
control_queue = Queue()
display_queue = Queue(maxsize=2)
display_template = 'image_server.html'

@app.route('/')
def index():
    return render_template(display_template)

def frame_generator():
    while True:
        time.sleep(0.03)    # < 30 fps
        encoded_bytes = display_queue.get()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encoded_bytes + b'\r\n')

@app.route('/display')
def display():
    return Response(frame_generator(), mimetype = 'multipart/x-mixed-replace; boundary=frame')

def start_server_process(template_name):
    global display_template
    display_template = template_name
    server = Process(target=app.run, kwargs={"host": "localhost","port": 5001})
    server.start()
    return server