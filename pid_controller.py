from lib2to3.pytree import NegatedPattern
import logging

logger = logging.getLogger("pid_controller")

class PIController:
    def __init__(self, proportional_constant=0, integral_constant=0, windup_limit=None):
        self.proportional_constant = proportional_constant
        self.integral_constant = integral_constant
        self.integral_sum = 0

        self.windup_limit = windup_limit

    def handle_proportional(self, error):
        return self.proportional_constant * error

    def handle_integral(self, error):
        lower_than_windup_limit = (abs(self.integral_sum) < self.windup_limit)
        negative_error = ((error > 0) != self.integral_sum > 0)

        if self.windup_limit is None or lower_than_windup_limit or negative_error:
            self.integral_sum += error
        return self.integral_constant * self.integral_sum

    def reset(self):
        self.integral_sum = 0

    def get_value(self, error):
        p = self.handle_proportional(error)
        i = self.handle_integral(error)
        logger.debug(f"P: {p}, I: {i:.2f}")
        return p + i

    