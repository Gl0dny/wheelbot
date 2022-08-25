from robot import Robot
from time import sleep

bot = Robot()
red = (255, 0 ,0)
blue = (0, 0, 255)
green = (0, 255, 0)

while True:
    print("Red")
    bot.leds.set_all(red)
    bot.leds.show()
    sleep(0.5)
    print("Blue")
    bot.leds.set_all(blue)
    bot.leds.show()
    sleep(0.5)
    # print("Green")
    # bot.leds.set_all(green)
    # bot.leds.show()
    # sleep(0.5)
    