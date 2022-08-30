from robot import Robot
import time
import logging
from gpiozero import DigitalInputDevice

logger = logging.getLogger("test_encoders")

class EncoderCounter(object):
    def __init__(self, pin_number):
        self.pulse_count = 0
        self.device = DigitalInputDevice(pin=pin_number)
        self.device.pin.when_changed = self.when_changed

    def when_changed(self, time_ticks, state):     
        self.pulse_count += 1


bot = Robot()
left_encoder = EncoderCounter(4)
right_encoder = EncoderCounter(26)