import logging

logger = logging.getLogger("pi_controller")

class PIController:
def __init__(self, proportional_constant=0, integral_constant=0):
    self.proportional_constant = proportional_constant
    self.integral_constant = integral_constant
    self.integral_sum = 0
