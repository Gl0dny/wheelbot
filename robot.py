from Raspi_MotorHAT import Raspi_MotorHAT as rpi_mh
from gpiozero import DistanceSensor
import atexit
import leds_led_shim
from servos import Servos
from encoder_counter import EncoderCounter

class Robot:
    #parameteres
    wheel_diameter_mm = 70.0
    encoders_shield_slits = 20.0
    ticks_per_revolution_multiplier = 2.0
    wheel_distance_mm = 140.0

    def __init__(self, motorhat_addr=0x60):

        self._mh = rpi_mh(addr=motorhat_addr)

        self.left_motor = self._mh.getMotor(1)
        self.right_motor = self._mh.getMotor(2)

        self.left_distance_sensor = DistanceSensor(echo=17, trigger=27, queue_len=2)
        self.right_distance_sensor = DistanceSensor(echo=5, trigger=6, queue_len=2)

        self.leds = leds_led_shim.Leds()

        self.servos = Servos(addr=motorhat_addr)    

        EncoderCounter.set_constants(self.wheel_diameter_mm, self.encoders_shield_slits, self.ticks_per_revolution_multiplier)
        self.left_encoder = EncoderCounter(4) #there is an issue for pin 4 both edge detection, one solution is -> 1-wire has to be disabled
        self.right_encoder = EncoderCounter(26)

        atexit.register(self.stop_all)
    
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
    
    def stop_all(self):
        self.stop_motors()
        self.leds.clear()
        self.leds.show()
        self.servos.stop_all()
        self.left_encoder.stop()
        self.right_encoder.stop()

    def set_left(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.left_motor.setSpeed(output_speed)
        self.left_motor.run(mode)

    def set_right(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.right_motor.setSpeed(output_speed)
        self.right_motor.run(mode)

    def set_pan(self, angle):
        self.servos.set_servo_angle(0, angle)

    def set_tilt(self, angle):
        self.servos.set_servo_angle(1, angle)