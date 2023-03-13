#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import snap7
import sqlite3
from snap7 import util
from threading import *

# Dictionary where to save the values readed from the PLC.
db_values = {'Auto': 0, 'Man': 0, 'Auditoria': 0, 'Error': 0, 'Ok': 0, 'Nok': 0, 'Error': []}

# Global variables to create flags and saved number created pieces.
writing_sql = False
num_ok = num_nok = 0
fabricated_ok = fabricated_nok = False

def convert_byte_to_bit(buffer):
    """
    Return all bits of the DB.
    Apply a mask to obtain the 16 bits of the DB:
    Ex: 1.0000.0000.0000.0000 OR 101 = 1.0000.0000.0000.0000.
    Ignore the MSB bit.
    """
    return bin(int.from_bytes(buffer, byteorder = 'little') | int('10000000000000000', 2))

def count_pieces(piece_ok, piece_nok):
    """
    Cuenta las piezas fabricadas, tanto OK como NOK.
    En el flanco de subida, cuenta la pieza y activa una señal.
    En el flanco de bajada, quita la señal para poder sumar la siguiente pieza.
    """
    global num_ok, num_nok, fabricated_ok, fabricated_nok

    if ((fabricated_ok == False) and (piece_ok == 1)):
        fabricated_ok = True
        num_ok += 1
    if ((fabricated_nok == False) and (piece_nok == 1)):
        fabricated_nok = True
        num_nok += 1
    if ((fabricated_ok == True) and (piece_ok == 0)):
        fabricated_ok = False
    if ((fabricated_nok == True) and (piece_nok == 0)):
        fabricated_nok = False

def write_sql(sql_connection, sql_cursor):
    """
    Write the values readed from PLC and saves it in the dictionary «db_values» in the database.
    Write in the database the values readed from PLC and saved in the dictionary «db_values». Then, reset «db_values» values.
    """
    global fabricated, num_ok, num_nok

    while True:
        # Start writing data to the SQL.
        writing_sql = True
        print(db_values)

        write_values_sql(sql_connection, sql_cursor, sql_query)

        # Reset values for read DB again.
        db_values.update({'Auto' : 0, 'Man' : 0, 'Auditoria' : 0, 'Error' : 0, 'Ok' : 0, 'Nok' : 0, 'Error' : [] })
        writing_sql = False
        num_ok = 0
        num_nok = 0
        time.sleep(3)


def read_db():
    """
    Read DB 91 and 100 from the PLC.
    """
    global num_ok, num_nok, fabricated_ok, fabricated_nok

    while True:

        if writing_sql == False:
            client = snap7.client.Client()

            try:
                client.connect('192.168.0.1', 0, 0)

                # If client is connected to the PLC, read DB and converts it to bit array.
                # Then, count pieces and write it to the dictionary «db_values».
                if (client.get_connected()):
                    read_db = client.db_read(91, 0, 2)
                    read_db_bin = convert_byte_to_bit(read_db)
                    count_pieces(int(read_db_bin[10]), int(read_db_bin[9]))
                    db_values.update({'Auto':int(read_db_bin[-1]),
                                      'Man':int(read_db_bin[-2]),
                                      'Auditoria':int(read_db_bin[-3]),
                                      'Error':int(read_db_bin[-4]),
                                      'Ok':num_ok,
                                      'Nok':num_nok,
                                      'Error':[]})

                else:
                    print("PLC disconnected.")

            except Exception as e:
                continue

        # Set a runtime delay.
        time.sleep(0.030)

def main():
    """
    Main program.
    Start connection to the SQLITE3.
    Call 2 trheads running concurrently in an infinite loop.
        - read_db()
        - write_sql().
    """
    # Start DB connection.
    sql_connection = sqlite3.connect(sql_path)
    sql_cursor = connection.cursor()

    # Create and start threats.
    read_db_thread = Thread(target = read_db)
    write_sql_thread = Timer(3, function = write_sql(sql_connection, sql_cursor))
    read_db_thread.start()
    write_sql_thread.start()

######################
# MAIN PROGRAM       #
######################
if __name__ == "__main__":
    print("RASPY-COM")
    main()
