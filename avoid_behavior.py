#!/usr/bin/python3
from robot import Robot
from time import sleep
from led_rainbow import show_rainbow

class ObstacleAvoidingBehavior:
    # Simple obstacle avoiding

    def __init__(self, the_robot):
        self.robot = the_robot
        self.speed = 40
        self.led_half = int(self.robot.leds.count/2)
        self.sense_colour = (255, 0, 0)
        

    def distance_to_led_bar(self, distance):
        inverted = max(0, 1.0 - distance)       #making sure there is no negative value
        led_bar = int(round(inverted * self.led_half)) + 1
        print(f"LED bar: {led_bar}")
        return led_bar

    def display_state(self, left_distance, right_distance):
        self.robot.leds.clear()
        led_bar = self.distance_to_led_bar(left_distance)
        # self.robot.leds.set_range(range(led_bar), self.sense_colour)
        show_rainbow(self.robot.leds, range(led_bar))

        led_bar = self.distance_to_led_bar(right_distance)
        start = (self.robot.leds.count - 1) - led_bar
        # self.robot.leds.set_range(range(start, self.robot.leds.count - 1), self.sense_colour)
        right_range = range(self.robot.leds.count - 1, start, -1)
        show_rainbow(self.robot.leds, right_range)

        self.robot.leds.show()    

    def get_speeds(self, nearest_distance):
        if nearest_distance >= 1.0:
            nearest_speed = self.speed
            furthest_speed = self.speed
            delay = 50
        elif nearest_distance >= 0.5:
            nearest_speed = self.speed
            furthest_speed = self.speed * 0.8
            delay = 50
        elif nearest_distance >= 0.2:
            nearest_speed = self.speed
            furthest_speed = self.speed * 0.6
            delay = 50
        elif nearest_distance >= 0.1:
            nearest_speed = -self.speed * 0.4
            furthest_speed = -self.speed 
            delay = 300
        else:
            #collision
            nearest_speed = -self.speed
            furthest_speed = -self.speed
            delay= 700
        return nearest_speed, furthest_speed, delay


    def run(self):
        # self.robot.set_pan(0)
        # self.robot.set_tilt(0)
        
        while True:
            left_distance = self.robot.left_distance_sensor.distance
            right_distance = self.robot.right_distance_sensor.distance

            self.display_state(left_distance, right_distance)

            nearest_speed, furthest_speed, delay = self.get_speeds(min(left_distance, right_distance ))
            print(f"Distances: Left: {left_distance:.2f}, Right: {right_distance:.2f}")
            print(f"Speeds: Nearest: {nearest_speed}, Furthest: {furthest_speed}")
            print(f"Pause: {delay}")

            if left_distance < right_distance:
                self.robot.set_left(nearest_speed)
                self.robot.set_right(furthest_speed)
            else:
                self.robot.set_left(furthest_speed)
                self.robot.set_right(nearest_speed)

            sleep(0.001 * delay)



bot = Robot()
behavior = ObstacleAvoidingBehavior(bot)
behavior.run()