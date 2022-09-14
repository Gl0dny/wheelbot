#!/usr/bin/python3
import time
import p_2war_hardware_abstraction_layer as HAL
import image_app_core as img_server

def controlled_image_server_behavior():
    camera = HAL.camera_stream.setup_camera()
    time.sleep(0.1)

    for frame in HAL.camera_stream.start_stream(camera):
        encoded_bytes = HAL.camera_stream.get_encoded_bytes_for_frame(frame)
        img_server.put_output_image(encoded_bytes)
