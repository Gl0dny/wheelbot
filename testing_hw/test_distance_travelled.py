from json import encoder
from robot import Robot
import time
import math
import logging

logger = logging.getLogger({"test_distance_travelled"})

wheel_diameter_mm = 70.0
encoders_shield_slits = 20.0
tick_per_revolution = 2 * encoders_shield_slits

ticks_to_mm_const = (math.pi * wheel_diameter_mm) / tick_per_revolution

def ticks_to_mm(ticks):
    return int(ticks_to_mm_const * ticks)