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
        assert os.path.exists(cascade_path), f"File {cascade_path} doesn't exist in the given cascade path"
        self.cascade = cv2.CascadeClassifier(cascade_path)
        #parameters
        self.center_x = 160 #hardcoded half of horizontal resolution
        self.center_y = 120 #hardcoded half of vertical resolution
        self.min_size = 20
        self.following = False
        #PIDs
        self.pan_pid = PIController(proportional_constant = 0.1, integral_constant = 0.03)
        self.tilt_pid = PIController(proportional_constant= -0.1, integral_constant = -0.03)

    def process_control(self):
        instruction = img_server.core.get_control_instruction()
        if instruction:
            command = instruction["command"]
            if command == "start":
                self.following = True
                print("Following...")
            elif command == "stop":
                self.following = False
                self.pan_pid.reset()
                self.tilt_pid.reset()
                self.robot.servos.stop_all()
                print("Following stopped.")
            if command == "exit":
                print("Color tracking stopped.")
                exit()      
    
    def find_object(self, original_frame):
        gray_img = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
        rectangles = self.cascade.detectMultiScale(gray_img)

        largest_rectangle = [0, (0, 0, 0, 0)]
        for (x, y, w, h) in rectangles:
            item_area = w * h
            if item_area > largest_rectangle[0]:
                largest_rectangle = ( int(item_area), (int(x), int(y), int(w), int(h)) )
        return largest_rectangle[1]

    def make_display(self, display_frame):
        encoded_bytes = img_server.camera_stream.get_encoded_bytes_for_frame(display_frame)
        img_server.core.put_output_image(encoded_bytes)

    def process_frame(self, frame):
        (x, y, w, h) = self.find_object(frame)
        cv2.rectangle(frame, (x, y), (x + w, y + w), (255, 0, 0), thickness = 2)
        self.make_display(frame)
        return x, y, w, h

    def run(self):
        self.robot.set_pan(0)
        self.robot.set_tilt(0)
        camera = img_server.camera_stream.setup_camera()
        time.sleep(0.1)
        self.robot.servos.stop_all()
        print("Configuration finished")

        for frame in img_server.camera_stream.start_stream(camera):
            (x, y, w ,h) = self.process_frame(frame)
            self.process_control()

            if self.following and h > self.min_size:
                pan_error = self.center_x - (x + (w/2))
                pan_value = self.pan_pid.get_value(pan_error)
                tilt_error = self.center_y - (y + (h/2))
                tilt_value = self.tilt_pid.get_value(tilt_error)

                self.robot.set_pan(int(pan_value))
                self.robot.set_tilt(int(tilt_value))

                print(f"X: {x}, Y: {y}, Width: {w}, Height: {h}, Pan error: {pan_error}, Pan value: {pan_value:.2f}, Tilt error:{tilt_error}, Tilt value: {tilt_value:.2f}")

print("Starting up face tracking..")
face_tracking = FaceTracking(Robot())
process = img_server.core.start_server_process("vision_tracking.html")
try:
    face_tracking.run()
finally:
    process.terminate()