#!/usr/bin/python3
import atexit
from pid_controller import PIController
from robot import Robot, EncoderCounter
import time
import logging

logger = logging.getLogger("drive_distance")

def drive_distance(bot, distance, speed=80):
    set_primary_motor = bot.set_left
    primary_encoder = bot.left_encoder
    set_secondary_motor = bot.set_right
    secondary_encoder = bot.right_encoder

    controller = PIController(proportional_constant=4, integral_constant=0.3)
    set_primary_motor(speed)
    set_secondary_motor(speed)

    while primary_encoder.pulse_count < distance or secondary_encoder.pulse_count < distance:
        time.sleep(0.01)
        error = primary_encoder.pulse_count - secondary_encoder.pulse_count
        adjustment = controller.get_value(error)
        set_primary_motor(int(speed - adjustment))
        set_secondary_motor(int(speed + adjustment))

        logger.debug(f"Encoders: primary: {primary_encoder.pulse_count}, secondary: {secondary_encoder.pulse_count},\nerror: {error}, adjustment: {adjustment:.2f}\n")
        logger.info(f"Distances: primary: {primary_encoder.distance_in_mm()} [mm], secondary: {secondary_encoder.distance_in_mm()} [mm]\n")

logging.basicConfig(level=logging.DEBUG)
bot = Robot()
distance_to_drive = 1000
distance_in_ticks = EncoderCounter.mm_to_ticks(distance_to_drive)
drive_distance(bot, distance_in_ticks) 
atexit