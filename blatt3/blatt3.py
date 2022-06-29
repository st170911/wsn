#!/usr/bin/python

from xbee import XBee
from sense_hat import SenseHat
import socket
import serial

rssi = []

sense = SenseHat()

def receive_data(response):
	#print("callback")
	if("rf_data" in response):
		if(response["rf_data"] == "ping"):
			xbee.send("tx",  frame_id="\x00", dest_addr="\x00\x02", data="pong")
			xbee.send("tx",  frame_id="\x00", dest_addr="\x00\x02", data="pong")
			xbee.send("tx",  frame_id="\x00", dest_addr="\x00\x02", data="pong")
			xbee.send("tx",  frame_id="\x00", dest_addr="\x00\x02", data="pong")
			xbee.send("tx",  frame_id="\x00", dest_addr="\x00\x02", data="pong")			
		if(response["rf_data"] == "pong"):
			rssi.append(ord(response["rssi"]))
			print(rssi)
			average = sum(rssi) / len(rssi)
			print(str(average))
			sense.show_message(str(average))
			if len(rssi) > 5:
				rssi.pop(0)

ser = serial.Serial('/dev/ttyUSB0', 9600)
xbee = XBee(ser, callback=receive_data)



try:
	while(True):
		for event in sense.stick.get_events():
			if event.action == "pressed":
				direction = event.direction
				if direction == "left":
					message = "ping"
					xbee.send("tx", frame_id="\x00", dest_addr="\x00\x02", data=message)
					print("Sent")				
				
except KeyboardInterrupt:
	sense.clear()
	ser.close()
#	print("Interrupted")



