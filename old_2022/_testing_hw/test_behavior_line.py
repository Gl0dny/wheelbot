#!/usr/bin/python3
import sys
sys.path.append('/home/pi/Projects/2-wheeled-autonomous-robot')
from time import sleep
from robot import Robot

r = Robot()
r.set_left(-30)
r.set_right(-30)
sleep(1)
