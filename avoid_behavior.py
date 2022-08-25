from ast import Return
from robot import Robot
from time import sleep

class ObstacleAvoidingBehavior:
    # Simple obstacle avoiding

    def __init__(self, the_robot):
        self.robot = the_robot
        self.speed = 60
    
    def get_speeds(self, nearest_distance):
        if nearest_distance >= 1.0:
            nearest_speed = self.speed
            furthest_speed = self.speed
            delay = 100
        elif nearest_distance >= 0.5:
            nearest_speed = self.speed
            furthest_speed = self.speed * 0.8
            delay = 100
        elif nearest_distance >= 0.2:
            nearest_speed = self.speed
            furthest_speed = self.speed * 0.6
            delay = 100
        elif nearest_distance >= 0.1:
            nearest_speed = -self.speed * 0.4
            furthest_speed = -self.speed 
            delay = 100
        else:
            #collision
            nearest_speed = -self.speed
            furthest_speed = -self.speed
            delay= 500
        return nearest_speed, furthest_speed, delay


    def run(self):
        # self.robot.set_pan(0)
        # self.robot.set_tilt(0)
        
        while True:
            left_distance = self.robot.left_distance_sensor.distance
            right_distance = self.robot.right_distance_sensor.distance

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