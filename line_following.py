#!/usr/bin/python3
import time
from xml.sax.handler import DTDHandler
import cv2
import numpy as np
import img_server
from pid_controller import PIController
from robot import Robot

class LineFollowing:
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
        #PIDs
        self.direction_pid = PIController(proportional_constant=0.4,integral_constant=0.01, windup_limit=400)

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

def find_line(self, frame):
    pass

def process_frame(self, frame):
    pass

def run(self):
    self.robot.set_pan(0)
    self.robot.set_tilt(50)
    camera = img_server.camera_stream.setup_camera()
    time.sleep(0.1)
    self.robot.servos.stop_all()
    print("Configuration finished.")

    last_time = time.time()

    for frame in img_server.camera_stream.start_stream(camera):
        x, magnitude = self.process_frame(frame)
        self.process_control()

        if self.following and magnitude > self.diff_threshold:
            direction_error = self.center - x
            new_time = time.time()
            dt = new_time - last_time
            direction_value = self.direction_pid.get_value(direction_error, delta_time = dt)
            last_time = new_time

            self.robot.set_left(self.speed - direction_value)
            self.robot.set_right(self.speed + direction_value)

            print(f"X: {x}, Peak diff: {magnitude}, Direction error: {direction_error}, Direction value: {direction_value:.2f}, Time: {new_time}")
        
        else:
            self.robot.stop_motors()
            if not self.following:
                self.direction_pid.reset()
            last_time = time.time()

print("Starting up line following...")
line_following = LineFollowing(Robot())
process = img_server.core.start_server_process("line_following.html")
try:
    line_following.run()
finally:
    process.terminate()