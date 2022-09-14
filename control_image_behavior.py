#!/usr/bin/python3
import time
import img_server

def controlled_image_server_behavior():
    camera = img_server.camera_stream.setup_camera()
    time.sleep(0.1)

    for frame in img_server.camera_stream.start_stream(camera):
        encoded_bytes = img_server.camera_stream.get_encoded_bytes_for_frame(frame)
        img_server.core.put_output_image(encoded_bytes)

        instruction = img_server.core.get_control_instruction()
        if instruction and instruction['command'] == "exit":
            print("Closing...")
            return None

process = img_server.core.start_server_process('control_image_behavior.html')
try:
    controlled_image_server_behavior()
finally:
    process.terminate()
