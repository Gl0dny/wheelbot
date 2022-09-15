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

    def process_control(self):
        instruction = img_server.core.get_control_instruction()
        if instruction:
            command = instruction["command"]
            if command == "start":
                self.motors_on = True
            elif command == "stop":
                self.motors_on == False
            elif command == "exit":
                print("Closing...")
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
                largest_circle = (int(x), int(y), int(radius))
                
        return masked_img, largest_circle[0], largest_circle[1]

    def make_display(self, frame, masked_frame):
        display_frame = np.concatenate((frame, masked_frame), axis = 1)
        encoded_bytes = img_server.camera_stream.get_encoded_bytes_for_frame(display_frame)
        img_server.core.put_output_image(encoded_bytes)