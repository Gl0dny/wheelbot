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
        #parameters
        self.center_x = 160 #hardcoded half of horizontal resolution
        self.center_y = 120 #hardcoded half of vertical resolution
        self.min_size = 20
        self.following = False
        #PIDs
        self.pan_pid = PIController(proportional_constant = 0.1, integral_constant = 0.03)
        self.tilt_pid = PIController(proportional_constant= -0.1, integral_constant = -0.03)
        

    def run(self):
        pass

print("Loading...")
face_tracking = FaceTracking(Robot())
process = img_server.core.start_server_process("vision_tracking.html")
try:
    face_tracking.run()
finally:
    process.terminate()