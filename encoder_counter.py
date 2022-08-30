from gpiozero import DigitalInputDevice

class EncoderCounter:
    def __init__(self, pin_number):
        self.pulse_count = 0
        self.direction = 1
        self.device = DigitalInputDevice(pin=pin_number)
        self.device.pin.when_changed = self.when_changed

    def when_changed(self, time_tick, state):
        self.pulse_count += self.direction