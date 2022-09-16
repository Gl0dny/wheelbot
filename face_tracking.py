#!/usr/bin/python3
import time
import cv2
import os
import img_server
from pid_controller import PIController
from robot import Robot

class FaceTracking:
    def __init__(self, robot):
        self.robot = robot
        #haar cascades
        cascade_path = "/home/pi/.local/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml"
        assert os.path.exists(cascade_path), f"File {cascade_path} doesn't exist in the give cascade path"
        self.scascade = cv2.CascadeClassifier(cascade_path)

    def run(self):
        pass

print("Loading...")
face_tracking = FaceTracking(Robot())
process = img_server.core.start_server_process("vision_tracking.html")
try:
    face_tracking.run()
finally:
    process.terminate()