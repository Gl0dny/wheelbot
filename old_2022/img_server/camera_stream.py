from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2

resolution = (320, 240)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def setup_camera():
    camera = PiCamera()
    camera.resolution = resolution
    camera.framerate = 30
    camera.rotation = 0
    return camera

def start_stream(camera):
    image_storage = PiRGBArray(camera, size=resolution)
    cam_stream = camera.capture_continuous(image_storage, format="bgr", use_video_port=True)
    for raw_frame in cam_stream:
        yield raw_frame.array
        image_storage.truncate(0)

def get_encoded_bytes_for_frame(frame):
    result, encoded_image = cv2.imencode('.jpg', frame, encode_param)
    return encoded_image.tostring()



