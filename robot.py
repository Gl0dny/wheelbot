from Raspi_MotorHAT import Raspi_MotorHAT as rpi_mh
from gpiozero import DistanceSensor

import atexit


class Robot:
    def __init__(self, motorhat_addr=0x60):

        self._mh = rpi_mh(addr=motorhat_addr)

        self.left_motor = self._mh.getMotor(1)
        self.right_motor = self._mh.getMotor(2)

        self.left_distance_sensor = DistanceSensor(echo=17, trigger=27, queue_len=2)
        self.right_distance_sensor = DistanceSensor(echo=5, trigger=6, queue_len=2)

        atexit.register(self.stop_motors)
    
    def convert_speed(self, speed):
        mode = rpi_mh.RELEASE
        if speed > 0:
            mode = rpi_mh.FORWARD
        elif speed < 0:
            mode = rpi_mh.BACKWARD

        output_speed = (abs(speed*255)) // 100
        return mode, int(output_speed)

    def stop_motors(self):
        self.left_motor.run(rpi_mh.RELEASE)
        self.right_motor.run(rpi_mh.RELEASE)

    def set_left(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.left_motor.setSpeed(output_speed)
        self.left_motor.run(mode)

    def set_right(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.right_motor.setSpeed(output_speed)
        self.right_motor.run(mode)
