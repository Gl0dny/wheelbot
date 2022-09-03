#!/usr/bin/python3
import sys
sys.path.insert(0, '/home/pi/Projects/2-wheeled-autonomous-robot')
from time import sleep
import robot

r = robot.Robot()
r.set_left(-30)
r.set_right(-30)
sleep(1)
