#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import snap7
from snap7 import util
from threading import *

# Dictionary where to save the values readed from the PLC.
db_values = {'Auto': 0, 'Man': 0, 'Auditoria': 0, 'Error': 0, 'Ok': 0, 'Nok': 0, 'Error': []}

# Sleep if the program write to SQL.
writing_sql = False
fabricated = False
num_ok = 0
num_nok = 0

def convert_byte_to_bit(buffer):
    """
    Return all bits of the DB.
    Apply a mask to obtain the 16 bits of the DB:
    Ex: 1.0000.0000.0000.0000 OR 101 = 1.0000.0000.0000.0000.
    Ignore the MSB bit.
    """
    # return bin(int.from_bytes((bytearray(b'\x00\x00\x01') or buffer), byteorder=sys.byteorder)).format(12)
    return bin(int.from_bytes(buffer, byteorder = 'little') | int('10000000000000000', 2))

def write_sql():
    """
    Write the velues readed from PLC and saved in the dictionary «db_values» in the database.
    """
    global fabricated, num_ok, num_nok
    while True:
        writing_sql = True
        print(db_values)
        db_values.update({'Auto' : 0, 'Man' : 0, 'Auditoria' : 0, 'Error' : 0, 'Ok' : 0, 'Nok' : 0, 'Error' : [] })
        writing_sql = False
        num_ok = 0
        num_nok = 0
        time.sleep(3)

def read_db():
    """
    Read DB 91 and 100 from the PLC.
    """
    global fabricated, num_ok, num_nok
    while True:
        if writing_sql == False:
            client = snap7.client.Client()
            try:
                client.connect('192.168.0.1', 0, 0)
                if (client.get_connected()):
                    read_db = client.db_read(91, 0, 2)
                    read_db_bin = convert_byte_to_bit(read_db)
                    # print(read_db_bin)
                    # print("OK: ", int(convert_byte_to_bit(read_db)[10]))
                    # print("NnnnnnOK: ", int(convert_byte_to_bit(read_db)[9]))
                    # if ((fabricated == False) and (int(read_db_bin[10]) == 1) or (int(read_db_bin[9]) == 1)):
                    if ((int(read_db_bin[10]) == 1) or (int(read_db_bin[9]) == 1)):
                        # print("PIECE FABRICATED")
                        fabricated = True
                    elif ((fabricated == True) and (int(read_db_bin[10]) == 0)):
                        print("--- ", num_ok)
                        num_ok += 1
                        fabricated = False
                    elif ((fabricated == True) and (int(read_db_bin[9]) == 0)):
                        print("###", num_nok)
                        num_nok += 1
                        fabricated = False
                    else:
                        pass
                    db_values.update({'Auto':int(read_db_bin[-1]), 'Man':int(read_db_bin[-2]), 'Auditoria':int(read_db_bin[-3]), 'Error':int(read_db_bin[-4]), 'Ok':num_ok, 'Nok':num_nok, 'Error':[]}) # int(read_db_bin[-9]), int(read_db_bin[-10]),
                else:
                    print("PLC disconnected.")
            except Exception as e:
                continue
        # Set a runtime delay.
        time.sleep(0.055)

def main():
    """
    Main program.
    Call 2 trheads running concurrently in an infinite loop.
    Call threads: read_db(), write_sql().
    """
    read_db_thread = Thread(target = read_db)
    write_sql_thread = Timer(3, function = write_sql)
    read_db_thread.start()
    write_sql_thread.start()

######################
# MAIN PROGRAM       #
######################
if __name__ == "__main__":
    print("RASPY-COM")
    main()
