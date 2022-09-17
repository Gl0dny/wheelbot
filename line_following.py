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
        self.middle_line_color = (128, 128, 255)
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

    def make_display(self, frame, middle, min_diff, max_diff, diff_list):
        cv2.line(frame, (self.center - 4, self.check_row), (self.center + 4, self.check_row), self.crosshair_color)
        cv2.line(frame, (self.center, self.check_row - 4), (self.center, self.check_row + 4), self.crosshair_color)
        cv2.line(frame, (middle, self.check_row - 8), (middle, self.check_row + 8), self.middle_line_color)
        cv2.line(frame, (min_diff, self.check_row - 4), (min_diff, self.check_row + 4), self.middle_line_color)
        cv2.line(frame, (max_diff, self.check_row - 4), (max_diff, self.check_row + 4), self.middle_line_color)

        graph_frame = np.zeros((img_server.camera_stream.size[1], img_server.camera_stream.size[0], 3), np.uint8)
        self.make_cv2_simple_graph(graph_frame, diff)

        display_frame = np.concatenate((frame, graph_frame), axis = 1)
        encoded_bytes = img_server.camera_stream.get_encoded_bytes_for_frame(display_frame)
        img_server.core.put_output_image(encoded_bytes)

    def make_cv2_simple_graph(self, frame, data):
        pass

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # blur = cv2.blue(gray, (5, 5))
        row = gray[self.check_row].astype(np.int32)
        diff = np.diff(row)
        max_diff = np.amax(diff, 0)
        min_diff = np.amin(diff, 0)

        if max_diff < 0 or min_diff > 0:
            return 0, 0

        min_diff_index = np.where(diff == min_diff)[0][0]
        max_diff_index = np.where(diff == max_diff)[0][0]
        middle = (min_diff_index + max_diff_index) // 2
        peak_diff = max_diff - min_diff

        self.make_display(frame, middle, min_diff, max_diff, diff)
        
        return middle, peak_diff

    def run(self):
        self.robot.set_pan(0)
        self.robot.set_tilt(50)
        camera = img_server.camera_stream.setup_camera()
        time.sleep(0.1)
        self.robot.servos.stop_all()
        print("Configuration finished.")

        last_time = time.time()

        for frame in img_server.camera_stream.start_stream(camera):
            x, peak_diff = self.process_frame(frame)
            self.process_control()

            if self.following and peak_diff > self.diff_threshold:
                direction_error = self.center - x
                new_time = time.time()
                dt = new_time - last_time
                direction_value = self.direction_pid.get_value(direction_error, delta_time = dt)
                last_time = new_time

                self.robot.set_left(self.speed - direction_value)
                self.robot.set_right(self.speed + direction_value)

                print(f"X: {x}, Peak diff: {peak_diff}, Direction error: {direction_error}, Direction value: {direction_value:.2f}, Time: {new_time}")
            
            else:
                self.robot.stop_motors()
                if not self.following:
                    self.direction_pid.reset()
                last_time = time.time()

print("Starting up line following...")
line_following = LineFollowing(Robot())
process = img_server.core.start_server_process("vision_tracking.html")
try:
    line_following.run()
finally:
    process.terminate()