#!/usr/bin/python3
from robot import Robot
import time
from pid_controller import PIController
import logging
logger = logging.getLogger("straight_line")
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("pi_controller").setLevel(logging.DEBUG)

bot=Robot()
stop_at_time = time.time() + 5
speed = 80
bot.set_left(speed)
bot.set_right(speed)

pi = PIController(proportional_constant=4, integral_constant=0.3)

while time.time() < stop_at_time:
    time.sleep(0.01)
    left = bot.left_encoder.pulse_count
    right = bot.right_encoder.pulse_count
    error = left - right
    adjustment = pi.get_value(error)
    right_speed = int(speed + adjustment)
    left_speed = int(speed - adjustment)

    logger.debug(f"error: {error}, adjustment: {adjustment:.2f}")
    logger.info(f"left: {left}, left_speed: {left_speed}\nright: {right}, right_speed: {right_speed}")

    bot.set_left(left_speed)
    bot.set_right(right_speed)