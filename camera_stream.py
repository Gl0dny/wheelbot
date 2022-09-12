from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2

size = (320,240)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def setup_camera():
    camera = PiCamera()
    camera.resolution = size
    cameraframerate = 30
    camera.rotation = 180
    return camera

def start_stream(camera):
    image_storage = PiRGBArray(camera, size=size)
    cam_stream = camera.capture_continous(image_storage, format="bgr", use_video_port = True)
    
def get_encoded_bytes_for_frame(frame):
    result, encoded_image = cv2.imencode('.jpg', frame, encode_param)
    return encoded_image.tostring()

for raw_frame in cam_stream:
    yield raw_frame.array
    image.storage.truncate(0)

