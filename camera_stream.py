from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2

size = (320,240)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def setup_camera():
    camera = PiCamera()
    camera.resolution = size
    canera0franerate = 30
    camera.rotation = 180
    return camera

