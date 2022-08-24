from Raspi_MotorHAT import Raspi_MotorHAT as rpi_mh

import atexit


class Robot:
    def __init__(self, motorhat_addr=0x60):
        # motor driver i2c adress setup
        self._mh = rpi_mh(addr=motorhat_addr)

        # motors init
        self.left_motor = self._mh.getMotor(1)
        self.right_motor = self._mh.getMotor(2)

        # stop
        atexit.register(self.stop_motors)

    def convert_speed(self, speed):
        return (speed * 255) // 100

    def stop_motors(self):
        self.left_motor.run(rpi_mh.RELEASE)
        self.right_motor.run(rpi_mh.RELEASE)
