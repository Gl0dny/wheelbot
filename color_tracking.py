#!/usr/bin/python3
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
        self.green_color_low_range = (35, 70, 25)  #HSV - Hue Saturation Value
        self.green_color_high_range = (80, 255, 255)
        self.correct_radius = 50 
        self.center = 160       #hardcoded half of horizontal resolution
        self.following = False

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
                print("Color tracking stopped.")
                exit()

    def find_object(self, original_frame):
        """Find the largest circle from all object countours.
        Output: masked img, object coordinates ( in pixels ), object circle radius"""

        frame_hsv = cv2.cvtColor(original_frame, cv2.COLOR_BGR2HSV)
        masked_img = cv2.inRange(frame_hsv, self.green_color_low_range, self.green_color_high_range)
        contours, _ = cv2.findContours(masked_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        circles = [cv2.minEnclosingCircle(cnt) for cnt in contours]

        largest_circle = [(0, 0), 0]
        for (x, y), radius in circles:
            if radius > largest_circle[1]:
                largest_circle = ( (int(x), int(y)), int(radius) )
                
        return masked_img, largest_circle[0], largest_circle[1]

    def make_display(self, frame, processed_frame):
        display_frame = np.concatenate((frame, processed_frame), axis = 1)
        encoded_bytes = img_server.camera_stream.get_encoded_bytes_for_frame(display_frame)
        img_server.core.put_output_image(encoded_bytes)

    def process_frame(self, frame):
        masked_img, coordinates, radius = self.find_object(frame)
        processed_frame = cv2.cvtColor(masked_img, cv2.COLOR_GRAY2BGR)
        cv2.circle(frame, coordinates, radius, (255, 0, 0), thickness = 2)
        self.make_display(frame, processed_frame)
        return coordinates, radius

    def run(self):
        self.robot.set_pan(0)
        self.robot.set_tilt(0)
        camera = img_server.camera_stream.setup_camera()
        speed_pid = PIController(proportional_constant=0.8, integral_constant=0.1, windup_limit=100)
        direction_pid = PIController(proportional_constant=0.25,integral_constant=0.05, windup_limit=400)
        time.sleep(0.1)
        self.robot.servos.stop_all()
        print("Configuration finished")
        
        for frame in img_server.camera_stream.start_stream(camera):
            (x, y), radius = self.process_frame(frame)
            self.process_control()
            if self.following and (radius > 5):
                #PID to control the distance between robot and the followed object
                radius_error = self.correct_radius - radius
                speed_value = speed_pid.get_value(radius_error)
                #PID to control the direction of robot's path to the followed object
                direction_error = self.center - x
                direction_value = direction_pid.get_value(direction_error)

                print("Radius, Radius Error, Speed Value, Direction Error, Direction Value")
                print(f"{radius}, {radius_error}, {speed_value:.2f}, {direction_error}, {direction_value:.2f}")

                self.robot.set_left(speed_value - direction_value)
                self.robot.set_right(speed_value + direction_value)
            else:
                self.robot.stop_motors()
                if not self.following:
                    speed_pid.reset()
                    direction_pid.reset()

print("Starting up color tracking...")
color_tracking = ColorTracking(Robot())
process = img_server.core.start_server_process("color_tracking.html")
try:
    color_tracking.run()
finally:
    process.terminate()
