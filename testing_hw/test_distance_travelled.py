#!/usr/bin/python3
import sys
sys.path.insert(0, '/home/pi/Projects/2-wheeled-autonomous-robot')
from robot import Robot
import time
import math
import logging

logger = logging.getLogger("test_distance_travelled")

wheel_diameter_mm = 70.0
encoders_shield_slits = 20.0
ticks_per_revolution = 2 * encoders_shield_slits

ticks_to_mm_const = (math.pi * wheel_diameter_mm) / ticks_per_revolution

def ticks_to_mm(ticks):
    return int(ticks_to_mm_const * ticks)

bot = Robot()
stop_at_time = time.time() + 1

logging.basicConfig(level=logging.INFO)
bot.set_left(90)
bot.set_right(90)

while time.time() < stop_at_time:
    logger.info("Left: {} [mm] Right: {} [mm]".format(
        ticks_to_mm(bot.left_encoder.pulse_count),
        ticks_to_mm(bot.right_encoder.pulse_count)))
    time.sleep(0.1)
    