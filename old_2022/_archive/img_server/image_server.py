#!/usr/bin/python3
from flask import Flask, render_template, Response
import p_2war_hardware_abstraction_layer as HAL
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('image_server.html')

def frame_generator():
    camera = HAL.camera_stream.setup_camera()
    time.sleep(0.1)

    for frame in HAL.camera_stream.start_stream(camera):
        encoded_bytes = HAL.camera_stream.get_encoded_bytes_for_frame(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encoded_bytes + b'\r\n')

@app.route('/display')
def display():
    return Response(frame_generator(), mimetype = 'multipart/x-mixed-replace; boundary=frame')

app.run(host="localhost", debug=True, port=5001)