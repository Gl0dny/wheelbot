#!/usr/bin/python3
from ssl import _PasswordType
import time
from tkinter import NONE
from xml.dom.minidom import parseString
import p_2war_hardware_abstraction_layer as HAL
import image_app_core as img_server

def controlled_image_server_behavior():
    camera = HAL.camera_stream.setup_camera()
    time.sleep(0.1)

    for frame in HAL.camera_stream.start_stream(camera):
        encoded_bytes = HAL.camera_stream.get_encoded_bytes_for_frame(frame)
        img_server.put_output_image(encoded_bytes)

        instruction = img_server.get_control_instruction()
        if instruction and instruction['command'] == "exit":
            print("Closing...")
            pass

process = img_server.start_server_process('control_image_behavior.html')
try:
    controlled_image_server_behavior()
finally:
    process.terminate()
