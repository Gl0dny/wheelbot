from time import sleep
from robot import Robot
from led_rainbow import show_rainbow

bot = Robot()

while True:
    print("LEDs on")
    show_rainbow(bot.leds, range(bot.leds.count))
    bot.leds.show()
    sleep(0.5)
    print("LEDs off")
    bot.leds.clear()
    bot.leds.show()
    sleep(0.5)