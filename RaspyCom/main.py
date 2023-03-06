#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import snap7
from snap7 import util

def convert_byte_to_bit(buffer):
	return bin(int.from_bytes(buffer, byteorder=sys.byteorder))

def main():
	while True:

		client = snap7.client.Client()

		# Connect to the PLC if the connection has not stablished.
		try:
			# PLC IP addres, rack, slot.
			client.connect('192.168.0.1', 0, 0)

		except Exception as e:
			print("PLC not connected to the Rapsberry Pi.", end=""),
			continue
	
		# Read PLC data and put it into DB.
		print("PLC connected.")
		read_db = client.db_read(91, 0, 2)
		
		print("DB readed data:\n---------------")
		# print(convert_byte_to_bit(read_db))
		print(convert_byte_to_bit(read_db)[0]),

		print(type(convert_byte_to_bit(read_db)[1]), end=""),
		print(type(convert_byte_to_bit(read_db)[2]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[3]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[4]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[5]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[6]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[7]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[8]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[9]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[10]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[11]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[12]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[13]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[14]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[15]), end=""),
		# # print(type(convert_byte_to_bit(read_db)[16])) 
		
		# Set a runtime delay.
		time.sleep(3)
	
######################
# MAIN PROGRAM       #
######################
if __name__ == "__main__":
	print("RASPY-COM")
	main()
