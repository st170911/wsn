#!/usr/bin/python3
from sense_hat import SenseHat
import socket
import serial

#ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=.5)
print("foo")
sense = SenseHat()

try:
	while(True):
		ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
#		print("asdf")
		for event in sense.stick.get_events():
			if event.action == "pressed":
#				print("pressed")
				direction = event.direction
				if direction == "up":
#					print("up")
					ser.write(bytes("{:.1f}".format(sense.get_temperature()), 'UTF-8'))
				if direction == "down":
       	                	        ser.write(bytes("{:.1f}".format(sense.get_humidity()), 'UTF-8'))
				if direction == "left":
       	                	        ser.write(bytes("{:.1f}".format(sense.get_pressure()), 'UTF-8'))
				if direction == "right":
       	                	        ser.write(bytes(socket.gethostname(), 'UTF-8'))
				if direction == "middle":
       	                	        ser.write("")

		message = str(ser.readline())
		if message != "b''":
			print(message)
			sense.show_message(message)
			sense.clear()
		ser.close()
except KeyboardInterrupt:
	sense.clear()
	ser.close()
#	print("Interrupted")

			
# to measure the pressure
# pressure = sense.get_pressure()

# to measure the temperature
# temp = sense.get_temperature()

# to measure the humidity
# humidity = sense.get_humidity()

# to show a message on the LED matrix
# sense.show_message("Hello world")

# to clear the LEDs
# sense.clear()


