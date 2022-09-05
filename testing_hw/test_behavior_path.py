#!/usr/bin/python3
import sys
sys.path.append('/home/pi/Projects/2-wheeled-autonomous-robot')
from robot import Robot
from time import sleep

def straight(bot, seconds):
    bot.set_left(50)
    bot.set_right(50)
    sleep(seconds)

def turn_left(bot, seconds):
    bot.set_left(20)
    bot.set_right(60)
    sleep(seconds)

def turn_right(bot, seconds):
    bot.set_left(60)
    bot.set_right(20)
    sleep(seconds)

def spin_left(bot, seconds):
    bot.set_left(-50)
    bot.set_right(50)
    sleep(seconds)


bot = Robot()
straight(bot, 0.5)
turn_right(bot, 0.5)
straight(bot, 0.5)
turn_left(bot, 0.5)
straight(bot, 0.5)
turn_left(bot, 0.5)
straight(bot, 0.5)
spin_left(bot, 3)