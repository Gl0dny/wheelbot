#!/usr/bin/python3
import atexit
from pid_controller import PIController
from robot import Robot, EncoderCounter
import time
import math
import logging

logger = logging.getLogger("drive_square")

def drive_distances(bot, left_distance, right_distance, speed=80):
    
    if abs(left_distance) >= abs(right_distance):
        logger.info("Left motor is the primary one")
        set_primary_motor = bot.set_left
        primary_encoder = bot.left_encoder
        set_secondary_motor = bot.set_right
        secondary_encoder = bot.right_encoder
        primary_distance = left_distance
        secondary_distance = right_distance
    else:
        logger.info("Right motor is the primary one")
        set_primary_motor = bot.set_right
        primary_encoder = bot.right_encoder
        set_secondary_motor = bot.set_left
        secondary_encoder = bot.left_encoder
        primary_distance = right_distance
        secondary_distance = left_distance

    primary_to_seconadry_ratio = secondary_distance / primary_distance
    secondary_speed = speed * primary_to_seconadry_ratio
    logger.debug(f"Distance to go: Primary: {primary_distance}, Secondary: {secondary_distance}, Ratio: {primary_to_seconadry_ratio:.2f}")

    primary_encoder.reset()
    secondary_encoder.reset()

    controller = PIController(proportional_constant=4, integral_constant=0.3)
    primary_encoder.set_direction(math.copysign(1, speed))
    secondary_encoder.set_direction(math.copysign(1, secondary_speed))
    set_primary_motor(speed)
    set_secondary_motor(speed)

    # while primary_encoder.pulse_count < distance or secondary_encoder.pulse_count < distance:
    #     time.sleep(0.01)
    #     error = primary_encoder.pulse_count - secondary_encoder.pulse_count
    #     adjustment = controller.get_value(error)
    #     set_primary_motor(int(speed - adjustment))
    #     set_secondary_motor(int(speed + adjustment))

    #     logger.debug(f"Encoders: primary: {primary_encoder.pulse_count}, secondary: {secondary_encoder.pulse_count},\nerror: {error}, adjustment: {adjustment:.2f}\n")
    #     logger.info(f"Distances: primary: {primary_encoder.distance_in_mm()} [mm], secondary: {secondary_encoder.distance_in_mm()} [mm]\n")

logging.basicConfig(level=logging.DEBUG)
bot = Robot()
distance_to_drive = 300
distance_in_ticks = EncoderCounter.mm_to_ticks(distance_to_drive)
radius = bot.wheel_distance_mm + 100
radius_in_ticks = EncoderCounter.mm_to_ticks(radius)

for n in range(4):
    drive_distances(bot, distance_in_ticks)
    drive_arc(bot, 90, radius_in_ticks, speed=50)

atexit