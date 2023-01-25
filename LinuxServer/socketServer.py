#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import socket
import json

json_received = """{"DI1":"0", "temps_DI1":"0","DI2":"0", "temps_DI2":"0","DI3":"0", "temps_DI3":"0","DI4":"0", "temps_DI4":"0","DI5":"0", "temps_DI5":"0", "DI6":"0", "temps_DI6":"0","DI7":"0", "temps_DI7":"0","DI8":"0", "temps_DI8":"0","DI9":"0", "temps_DI9":"0","DI10":"0", "temps_DI10":"0"}"""
db_path = "/home/admin/TFG/esp32.db"
db_query = "INSERT INTO esp32_table (Data,Ok,TempsOK,NOK,TempsNOK,Auto,Error,TempsError,DI5,TempsDI5,DI6,TempsDI6,DI7,TempsDI7,DI8,TempsDI8,DI9,TempsDI9,DI10,TempsDI10) VALUES (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)"

print("""
##########################################################
# CREATE A SOCKET SERVER                                 #
# ------------------------------------------------------ #
# We connect the ESP32 with this server writed with      #
# Python. Send the data to this server, and then process #
# it and saves the data in a DB writed with SQL.         #
##########################################################
""")

'''
JSON DICTIONARY PYTHON
'''
def convert_json_to_query(json_msg):
	# Convert json_msg to dictionary.
	print(type(json_msg))
	print("___", json_msg, "___");
	json_d = json.loads(json_msg)

	# Create 3 string for columns and her values.
	columns = ""
	values = ""
	for key, value in json_d.items():

		columns += key + ","
		values += value + ","

	# Create query.
	return "INSERT INTO esp32_table (" + columns[:-1] + ") VALUES (" + values[:-1] + ")"

def insert_query_db(con, cursor, query):
	try:
		cursor.execute(query)
		con.commit()
		print("Query inserted correctly in DB.");
		return True
	except Exception as ex:
		print("AN ERROR OCURRED: ", ex)
		return False

'''
SOCKET CONNECTION AND TRANSFERING ESP32 -> PYTHON SOCKET SERVER LINUX
'''

def main():
	
	# Configure the socket.
	s = socket.socket()
	
	# s.bind(("192.168.1.107", 4554))
	s.bind(("0.0.0.0", 4554))
	
	# Start the listening.
	s.listen(3)

	# At the same time, connects the program to the BD to later save the values sended by ESP32.
	connection = sqlite3.connect(db_path)
	cursor = connection.cursor()
	
	while True:
	
		# Accept the server.
		client, addr = s.accept();
		k = 0;
	
		while True:
	
			content = client.recv(600);
	
			if (len(content) <= 0):
				break
	
			if ("DI1" in str(content)):
				print("Content:\n", content, "\n--- --- ---")
				print("\n==================================\n")
				print(convert_json_to_query(content))
				query_db = convert_json_to_query(content)
				print(type(content))
				insert_query_db(connection, cursor, query_db)
				print("\n==================================\n")
				k += 1
	
	
		print("Client desconnected.")
		client.close()
	
		if (k != 0):
			break

# ----------------------------------------------------------------------------- #
# MAIN PROGRAM                                                                  #
# Executed only if the script has been executed as the main program.            #
# ----------------------------------------------------------------------------- #
if __name__ == "__main__":
        main()
