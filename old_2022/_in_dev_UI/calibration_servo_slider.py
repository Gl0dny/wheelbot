#!/usr/bin/python3
from gpiozero import AngularServo
from guizero import App, Slider

servo = AngularServo(18, initial_angle = 0.0, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000)

def slider_changed(angle):
    servo.angle = int(angle)

app = App(title="Servo calibration", width=500, height=150)
slider = Slider(app, start=-90, end=90, command = slider_changed, width='fill', height=50)
slider.test_size = 30
app.display()