#!/usr/bin/python3
from pid_controller import PIController
from robot import Robot
from p_2war_hardware_abstraction_layer import EncoderCounter
import time
import math
import logging

logger = logging.getLogger("drive_square")

def _drive_distances(bot, left_distance, right_distance, speed=80):
    
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

    secondary_to_primary_ratio = secondary_distance / primary_distance
    secondary_speed = speed * secondary_to_primary_ratio
    logger.debug(f"Distance to go: Primary: {primary_distance}, Secondary: {secondary_distance}, Ratio: {secondary_to_primary_ratio:.2f}")

    primary_encoder.reset()
    secondary_encoder.reset()

    controller = PIController(proportional_constant=5, integral_constant=0.2)
    primary_encoder.set_direction(int(math.copysign(1, speed)))
    secondary_encoder.set_direction(int(math.copysign(1, secondary_speed)))
    set_primary_motor(speed)
    set_secondary_motor(int(secondary_speed))

    while abs(primary_encoder.pulse_count) < abs(primary_distance) or abs(secondary_encoder.pulse_count) < abs(secondary_distance):
        time.sleep(0.01)
        secondary_target = primary_encoder.pulse_count * secondary_to_primary_ratio
        error = secondary_target - secondary_encoder.pulse_count
        adjustment = controller.get_value(error)
        set_secondary_motor(int(secondary_speed + adjustment))
        secondary_encoder.set_direction(math.copysign(1, secondary_speed+adjustment))


        logger.debug(f"Encoders: primary: {primary_encoder.pulse_count}, secondary: {secondary_encoder.pulse_count},\nerror: {error}, adjustment: {adjustment:.2f}\n")
        logger.info(f"Distances: primary: {primary_encoder.distance_in_mm()} [mm], secondary: {secondary_encoder.distance_in_mm()} [mm]\n")

        if abs(primary_encoder.pulse_count) >= abs(primary_distance):
            logger.info("Primary motor stopped")
            set_primary_motor(0)
            secondary_speed = 0        

def drive_arc(bot, turn_in_degrees, radius, arc_speed=80):
    half_width_ticks = EncoderCounter.mm_to_ticks(bot.wheel_distance_mm / 2.0)
    
    if turn_in_degrees < 0:
        left_radius = radius - half_width_ticks
        right_radius = radius + half_width_ticks
    elif turn_in_degrees > 0:
        left_radius = radius + half_width_ticks
        right_radius = radius - half_width_ticks
    
    turn_in_radians = math.radians(abs(turn_in_degrees))
    left_distance = int(left_radius * turn_in_radians)
    right_distance = int(right_radius * turn_in_radians)

    _drive_distances(bot, left_distance, right_distance, speed = arc_speed)

    logger.info(f"Left arc radius: {left_radius:.2f} [mm], Right arc radius: {right_radius:.2f} [mm]")
    
logging.basicConfig(level=logging.DEBUG)
bot = Robot()
radius = bot.wheel_distance_mm + 50
radius_in_ticks = EncoderCounter.mm_to_ticks(radius)
arc_degree = 90
speed = 50


for n in range(4):
    drive_arc(bot, arc_degree, radius_in_ticks, speed)
