#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import snap7
from snap7 import util
from threading import *

# Dictionary where to save the values readed from the PLC.
db_values = {'Auto': 0, 'Man': 0, 'Auditoria': 0, 'Error': 0, 'Ok': 0, 'Nok': 0, 'Error': []}

fabricated = False
num_ok = num_nok = 0

def convert_byte_to_bit(buffer):
    # return bin(int.from_bytes((bytearray(b'\x00\x00\x01') or buffer), byteorder=sys.byteorder)).format(12)
    return bin(int.from_bytes(buffer, byteorder = 'little') | int('10000000000000000', 2))

def read_db():
    global fabricated, num_ok, num_nok
    while True:
        client = snap7.client.Client()
        try:
            client.connect('192.168.0.1', 0, 0)
            if (client.get_connected()):
                read_db = client.db_read(91, 0, 2)
                read_db_bin = convert_byte_to_bit(read_db)
                print(read_db)
                print(type(read_db_bin))
                if (read_db_bin[-9] == '1'):
                    print("OKAY")
                if (read_db_bin[-10] == '1'):
                    print("NO OKAY")
                else:
                    print("Else")
                """
                if ((fabricated == False) and (int(read_db_bin[-9]) == 1) or (int(read_db_bin[-10]) == 1)):
                    print("PIECE FABRICATED")
                    fabricated = True
                elif ((fabricated == True) and (int(read_db_bin[-9]) == 0)):
                    # db_values['Ok'] += 1
                    print("Piece OK fabricated.")
                    print(num_ok)
                    num_ok += 1
                    fabricated = False
                elif ((fabricated == True) and (int(read_db_bin[-10]) == 0)):
                    # db_values['Nok'] += 1
                    print("Piece NOK fabricated.")
                    print(num_nok)
                    num_nok += 1
                    fabricated = False
                else:
                    pass
                db_values.update({'Auto':int(read_db_bin[-1]), 'Man':int(read_db_bin[-2]), 'Auditoria':int(read_db_bin[-3]), 'Error':int(read_db_bin[-4]), 'Ok':num_ok, 'Nok':num_nok, 'Error':[]}) # int(read_db_bin[-9]), int(read_db_bin[-10]),
                """
            else:
                print("PLC disconnected.")
        except Exception as e:
            continue


    # Set a runtime delay.
    time.sleep(0.055)

read_db()

"""
while True:

if (writing_sql == False):
    client = snap7.client.Client()

    try:
        # PLC IP addres, rack, slot.
        client.connect('192.168.0.1', 0, 0)

        # If the PLC is connected, update the «db_values» dictionary.
        if (client.get_connected()):
            read_db = client.db_read(91, 0, 2)
            read_db_bin = convert_byte_to_bit(read_db)
            # TODO
            # print("###")
            # print("--- ", int(convert_byte_to_bit(read_db)[-8]), end = " ---\n")
            # print("--- ", int(convert_byte_to_bit(read_db)[-9]), end = " ---\n")
            # print("--- ", int(convert_byte_to_bit(read_db)[-10]), end = " ---\n")
            # print("###")
            # TODO

            # TODO: We can encapsulate this code.
            # Check if a part has been manufactured (bit to '1').
            if ((int(read_db_bin[-9]) == 1) or (int(read_db_bin[-10]) == 1)):
                print("PIECE FABRICATED")
                fabricated = True
            # When there is a falling edge on the OKAY bit of the db, a piece has manufactured.
            elif ((fabricated == True) and (int(read_db_bin[-9]) == 0)):
                # db_values['Ok'] += 1
                print("Piece OK fabricated.")
                num_ok += 1
                fabricated = False
            elif ((fabricated == True) and (int(read_db_bin[-10]) == 0)):
                # db_values['Nok'] += 1
                print("Piece NOK fabricated.")
                num_nok += 1
                fabricated = False
            else:
                pass
            # TODO

            db_values.update({'Auto':int(read_db_bin[-1]),
                              'Man':int(read_db_bin[-2]),
                              'Auditoria':int(read_db_bin[-3]),
                              'Error':int(read_db_bin[-4]),
                              'Ok':num_ok, # int(read_db_bin[-9]),
                              'Nok':num_nok, # int(read_db_bin[-10]),
                              'Error':[]
                              })

        else:
            print("PLC disconnected.")

    except Exception as e:
        # print("PLC not connected to the Rapsberry Pi."),
        continue

else:
    print("Writing to the DB.")

# Set a runtime delay.
time.sleep(0.055)
"""
