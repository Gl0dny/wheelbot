import robot
from Raspi_MotorHAT import Raspi_MotorHAT as rpi_mh
from time import sleep

r = robot.Robot()
r.left_motor.setSpeed(r.convert_speed(80))
r.right_motor.setSpeed(r.convert_speed(80))
r.left_motor.run(rpi_mh.FORWARD)
r.right_motor.run(rpi_mh.FORWARD)
sleep(1)
