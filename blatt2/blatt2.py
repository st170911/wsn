#!/usr/bin/python3
from sense_hat import SenseHat
import socket

sense = SenseHat()

while(True):
	for event in sense.stick.get_events():
		if event.action == "pressed":
			direction = event.direction
			if direction == "up":
				sense.show_message("{:.1f}".format(sense.get_temperature()))
			if direction == "down":
                                sense.show_message("{:.1f}".format(sense.get_humidity()))
			if direction == "left":
                                sense.show_message("{:.1f}".format(sense.get_pressure()))
			if direction == "right":
                                sense.show_message(socket.gethostname())
			if direction == "middle":
                                sense.clear()


			
# to measure the pressure
pressure = sense.get_pressure()

# to measure the temperature
temp = sense.get_temperature()

# to measure the humidity
humidity = sense.get_humidity()

# to show a message on the LED matrix
sense.show_message("Hello world")

# to clear the LEDs
sense.clear()


