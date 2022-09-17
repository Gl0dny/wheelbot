#!/usr/bin/python3
import time
import cv2
import numpy as np
import img_server
from pid_controller import PIController
from robot import Robot

class LineFollwing:
    def __init__(self, robot):
        self.robot = robot
        #line following parameteres
        self.check_row = 180
        self.diff_threshold = 10
        self.center = 160
        self.following = False
        self.speed = 50
        