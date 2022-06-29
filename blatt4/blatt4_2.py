#!/usr/bin/python

from xbee import XBee
from sense_hat import SenseHat
import socket
import serial
import datetime
import sys

measuring = sys.argv[1]
print(measuring)

rssi = []
n = 2.8
A = 35
# "geeichte" (haha c:) Werte
_x = "1"
_y = "1"
neighbors = {}
neighbors_coord = {}

sense = SenseHat()

def receive_data(response):
	#print("callback")
	if("rf_data" in response):
		if(response["rf_data"] == "ping"):
			xbee.send("tx",  frame_id="\x00", dest_addr="\x00\x02", data=_x + "," + _y)
		if(response["rf_data"] != "ping"):
			source = response["source_addr"]
			rssi = ord(response["rssi"])
			distance = 10**((A-rssi)/(10*n))
			neighbors[source] = distance
			neighbors_coord[source] = response["rf_data"]
			
			
				

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
				
				if direction == "right":
					max_x = max(neighbors, key=neighbors.get()) 
					min_x = min(neighbors, key=neighbors.get()) 
					max_y = max(neighbors, key=neighbors.get()) 
					min_y = min(neighbors, key=neighbors.get()) 
					x = 0.5 * 
				
				
except KeyboardInterrupt:
	sense.clear()
	ser.close()
	print("Interrupted")







