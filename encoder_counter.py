from gpiozero import DigitalInputDevice
import math

class EncoderCounter:
    ticks_to_mm_const = None

    def __init__(self, pin_number):
        self.pulse_count = 0
        self.direction = 1
        self.device = DigitalInputDevice(pin=pin_number)
        self.device.pin.when_changed = self.when_changed

    def when_changed(self, time_tick, state):
        self.pulse_count += self.direction

    def set_direction(self, direction):
        """Expected value: 1 or -1"""
        assert abs(direction)==1, "Direction %s should be set to 1 or -1" %direction
        self.direction = direction

    def reset(self):
        self.pulse_count = 0

    def stop(self):
        self.device.close()

    def distance_in_mm(self):
        #distance value taken from class, not it's instance (constant diameter and number of slits)
        return int(self.pulse_count * EncoderCounter.ticks_to_mm_const) 
    
    @staticmethod
    #static method so the distance value can be converted to ticks without creating instance
    def mm_to_ticks(mm):
        return mm / EncoderCounter.ticks_to_mm_const

    @staticmethod
    def set_constants(wheel_diameter_mm, encoders_shield_slits, ticks_per_revolution_multiplier):
        EncoderCounter.ticks_to_mm_const = (math.pi * wheel_diameter_mm) / (encoders_shield_slits*ticks_per_revolution_multiplier)
        