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
        #colors
        self.crosshair_color = (0, 255, 0)
        self.line_middle_color = (128, 128, 255)
        self.graph_color = (255, 128, 128)

def process_control(self):
        instruction = img_server.core.get_control_instruction()
        if instruction:
            command = instruction["command"]
            if command == "start":
                self.following = True
                print("Following...")
            elif command == "stop":
                self.following = False
                print("Following stopped.")
            if command == "exit":
                print("Line following stopped.")
                exit()