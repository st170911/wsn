#!/usr/bin/python

from xbee import XBee
from sense_hat import SenseHat
import socket
import serial
import datetime

now = datetime.datetime.now
time1 = now()

#rssi = []

sense = SenseHat()

b_data = "ping"
b_reply = "pong"
f_header = "Fw: "

neighbors = {}

def receive_data(response):
	#print("callback")
	if("rf_data" in response):
		#if(response["rf_data"] == "ping"):
		#	xbee.send("tx",  frame_id="\x00", dest_addr="\x00\x02", data="pong")
		#	xbee.send("tx",  frame_id="\x00", dest_addr="\x00\x02", data="pong")
		#	xbee.send("tx",  frame_id="\x00", dest_addr="\x00\x02", data="pong")
		#	xbee.send("tx",  frame_id="\x00", dest_addr="\x00\x02", data="pong")
		#	xbee.send("tx",  frame_id="\x00", dest_addr="\x00\x02", data="pong")			
		
		#if(response["rf_data"] == "pong"):
		#	rssi.append(ord(response["rssi"]))
		#	print(rssi)
		#	average = sum(rssi) / len(rssi)
		#	print(str(average))
		#	sense.show_message(str(average))
		#	if len(rssi) > 5:
		#		rssi.pop(0)
		
		#broadcast
		if(response["rf_data"] == "ping"):
			print("received broadcast")
			source = response["source_addr"]
			xbee.send("tx",  frame_id="\x00", dest_addr=source, data="pong")
		
		#broadcast response	
		elif(response["rf_data"] == "pong"):
			source = response["source_addr"]
			#print("1")
			#print("received response")
			rssi = ord(response["rssi"])
			#print("2")
			neighbors[source] = rssi
			#print(neighbors)
			
		#handle messages
		elif(response["rf_data"] != b_data and response["rf_data"] != "pong"):
			#message = response["rf_data"]
			print(str(message))
			if (message[0:4] == f_header):
				print("received message " + message)
				sense.show_message(message)
			else:
				message = f_header + message
				source = response["source_addr"]
				print("forwarded " + message)
				for neighbor in neighbors:
						if neighbor != source:
							xbee.send("tx",  frame_id="\x00", dest_addr=neighbor, data=message)
		else:
			print(response)	
			


ser = serial.Serial('/dev/ttyUSB0', 9600)
xbee = XBee(ser, callback=receive_data)

def broadcast():
	broadcast = "\xFF\xFF"
	print("sent broadcast ping")
	xbee.send("tx",  frame_id="\x00", dest_addr=broadcast, data="ping")


try:
	while(True):
		
		time2 = now()
		t_diff = time2 - time1
		
		if (t_diff.seconds > 2):
			time1 = now()
			broadcast()
		
		for event in sense.stick.get_events():
			if event.action == "pressed":
				direction = event.direction
				#if direction == "left":
				#	message = "ping"
				#	xbee.send("tx", frame_id="\x00", dest_addr="\x00\x02", data=message)
				#	print("Sent")		

				if direction == "middle":
					# send to best neighbor	
					signal_strength = 200
					strongest_neighbor = ""
					for neighbor in neighbors:
						neighbor_strength = neighbors[neighbor]
						if neighbors[neighbor] < signal_strength:
							signal_strength = neighbor_strength
							strongest_neighbor = neighbor
					if strongest_neighbor != "":
						message = "{:.1f}".format(sense.get_temperature())
						xbee.send("tx", frame_id="\x00", dest_addr=strongest_neighbor, data=message)
						print("sent message: " + str(message))
					
						
						
				
except KeyboardInterrupt:
	sense.clear()
	ser.close()
#	print("Interrupted")



