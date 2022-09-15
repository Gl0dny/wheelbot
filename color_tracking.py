#!usr/bin/python3
import time
import cv2
import numpy as np
import img_server
from pid_controller import PIController
from robot import Robot

class ColorTracking:
    def __init__(self, robot):
        self.robot = robot
        #object parameters:
        self.green_color_low_range = (35, 102, 25)  #HSV - Hue Saturation Value
        self.green_color_high_range = (80, 255, 255)
        self.correct_radius = 50   
        self.center = img_server.camera_stream.resolution // 2 
        self.motors_on = False

        

        