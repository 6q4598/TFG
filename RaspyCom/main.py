#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import snap7
import sqlite3
import os
import OEE
from datetime import datetime
from snap7 import util
from threading import *

# Dictionary where to save the values readed from the PLC.
db_values = {'Auto': 0, 'Man': 0, 'Audit': 0, 'Error': 0, 'Maintenance': 0, 'Ok': 0, 'Nok': 0, 'ErrorCodes': ''}

# Global variables to create flags and saved number created pieces.
# TODO: writing_sql = False
num_ok = num_nok = 0
fabricated_ok = fabricated_nok = False
db_sleep = 10
plc_sleep = 0.030

# SQLite3 PATH and creation table strings.
sql_path = "/media/rpiiot/CCCOMA_X64F/4246_IOT.db"
create_table_plc = "CREATE TABLE table_plc (Date TIME, Hour TIME, Auto INTEGER, Manual INTEGER, Audit INTEGER, Error INTEGER, Maintenance INTGER, Ok INTEGER, NOk INTEGER, Error_codes TEXT, PRIMARY KEY (Date, Hour))"
create_table_shifts = "CREATE TABLE table_shifts (Id INTEGER, Days STRING, Start_time TIME, End_time TIME, Break_time INTEGER, PRIMARY KEY (id))"
create_table_oee = "CREATE TABLE table_oee (Date TIME, Hour TIME, Oee REAL, Availability REAL, Performance REAL, Quality REAL, PRIMARY KEY (Date, Hour))"

"""
---------------------------------------
OEE FUNCTIONS
---------------------------------------
- Get the total time of the current shift.
- Get: Start hour, end hour, total number of hours of the current shift.
- Get: The number of hours until now in the current shift.
- Get: The number of intervals has passed.
---------------------------------------
"""
def get_count_num_intervals(sql_connection, sql_cursor):
    """
    Function that returns the number of intervals has passed.
    Consider the time between two intervals the time elapsed between the writing
    of two records in the database.
    We can get the toal time elapsed by multiplying the number of intervals that have
    passed since the start of shift by the time that elapses between writing 2 records
    to the database.
    """
    sql_query = "SELECT COUNT(*) FROM table_plc WHERE Hour > {} AND Hour < {} AND Date = '{}'".format(
        get_start_shift_hour(sql_connection, sql_cursor),
        get_start_end_hour(sql_connection, sql_cursor),
        time.strftime("%D")
    )


def get_start_shift_hour(sql_connection, sql_cursor):
    """
    Function that returns the start hour of the current shift.
    Current shift is determine dy the day of the week and the time we are in.
    """
    sql_query = "SELECT TODO FROM table_shifts WHERE days LIKE '%{}%' AND Start_time < '{}' AND End_time > '{}'".format(
        time.strftime("%A"), current_hour, time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S")
    )
    try:
        sql_cursor.execute(sql_query)
        sql_connection.commit()
    except sqlite3.OperationalError as e:
        print("Error to get the start time of the shift. Error: ", e)

def get_start_shift_hour(sql_connection, sql_cursor):
    """
    Function that returns the start hour of the current shift.
    Current shift is determine dy the day of the week and the time we are in.
    """
    sql_query = "SELECT TODO FROM table_shifts WHERE days LIKE '%{}%' AND Start_time < '{}' AND End_time > '{}'".format(
        time.strftime("%A"), current_hour, time.strftime("%H:%M:%S"), time.strftime("%H:%M:%S")
    )
    try:
        sql_cursor.execute(sql_query)
        sql_connection.commit()
    except sqlite3.OperationalError as e:
        print("Error to get the start time of the shift. Error: ", e)


"""
---------------------------------------
COMPLEMENTARY FUNCTIONS
---------------------------------------
"""

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
        print(num_ok, " <<<")
    if ((fabricated_nok == False) and (piece_nok == 1)):
        fabricated_nok = True
        num_nok += 1
        print(num_nok, " <<<")
    if ((fabricated_ok == True) and (piece_ok == 0)):
        fabricated_ok = False
    if ((fabricated_nok == True) and (piece_nok == 0)):
        fabricated_nok = False

def write_values_sql(sql_connection, sql_cursor, sql_query):
    """
    Insert values. Executes «sql_query».
    """
    print(sql_query)
    try:
        sql_cursor.execute(sql_query)
        sql_connection.commit()
    except sqlite3.OperationalError as e:
        print("Error to write the PLC values to the database. Error: ", e)

def create_tables(sql_cursor):
    """
    Create a database if not exists.
    """
    try:
        sql_cursor.execute(create_table_plc)
        sql_cursor.execute(create_table_shifts)
        sql_cursor.execute(create_table_oee)
    except:
        print("Creating tables error. Error: ", e)

"""
---------------------------------------
THREADS FUNCTIONS
---------------------------------------
"""

# TODO:
#def write_sql(sql_connection, sql_cursor):
def write_sql():
    """
    Write the values readed from PLC and saves it in the dictionary «db_values» in the database.
    Write in the database the values readed from PLC and saved in the dictionary «db_values». Then, reset «db_values» values.
    """
    global fabricated, num_ok, num_nok

    # Start DB connection. If the database not exists, create tables.
    if (os.path.exists(sql_path)):
        print("Connect to the database.")
        sql_connection = sqlite3.connect(sql_path)
        sql_cursor = sql_connection.cursor()
    else:
        print("Create database.")
        sql_connection = sqlite3.connect(sql_path)
        sql_cursor = sql_connection.cursor()
        create_tables(sql_cursor)

    while True:
        # Save current PLC values and reset values for read DB again. WARNING: python memory when «=».!!!
        db_values_temp = {'Auto': db_values['Auto'], 'Man': db_values['Man'], 'Audit': db_values['Audit'],
                          'Error': db_values['Error'], 'Maintenance': db_values['Maintenance'],
                          'Ok': db_values['Ok'], 'Nok': db_values['Nok'], 'ErrorCodes': db_values['ErrorCodes']}
        num_ok_temp = num_ok
        num_nok_temp = num_nok
        db_values.update({'Auto' : 0, 'Man' : 0, 'Audit' : 0, 'Error' : 0, 'Maintenance': 0, 'Ok' : 0, 'Nok' : 0, 'ErrorCodes' : '' })
        num_ok = 0
        num_nok = 0
        print(num_ok, " --------- ", num_ok_temp)
        print(num_nok, " --------- ", num_nok_temp)

        # Start writing data to the SQL.
        # TODO: Falta afegir els valors per a la columna Errors (DB 100).
        sql_query = "INSERT INTO table_plc (Date,Hour,Auto,Manual,Audit,Error,Maintenance,Ok,Nok) VALUES ('{}','{}',{},{},{},{},{},{},{})".format(
            datetime.today().strftime('%D'), datetime.today().strftime('%H:%M:%S'),
            db_values_temp['Auto'], db_values_temp['Man'], db_values_temp['Audit'], db_values_temp['Error'],
            db_values_temp['Maintenance'], num_ok_temp, num_nok_temp) # TODO: db_values_temp['Error'])

        # Insert values readed from the PLC to the database.
        write_values_sql(sql_connection, sql_cursor, sql_query)
        time.sleep(db_sleep)

def read_plc():
    """
    Read DB 91 and 100 from the PLC.
    """
    global num_ok, num_nok, fabricated_ok, fabricated_nok

    while True:

        client = snap7.client.Client()

        try:
            client.connect('192.168.0.1', 0, 0)

            if (client.get_connected()):
                # If client is connected to the PLC, read DB and converts it to bit array.
                read_plc = client.db_read(91, 0, 2)
                read_plc_bin = convert_byte_to_bit(read_plc)
                # Then, count pieces and write it to the dictionary «db_values».
                count_pieces(int(read_plc_bin[10]), int(read_plc_bin[9]))
                db_values.update({'Auto': int(read_plc_bin[-1]), 'Man': int(read_plc_bin[-2]), 'Audit': int(read_plc_bin[-3]),
                                  'Error': int(read_plc_bin[-4]), 'Maintenance': int(read_plc_bin[-5]), 'Ok': num_ok,
                                  'Nok': num_nok, 'ErrorCodes': ''})
            else:
                print("PLC disconnected.")

        except Exception as e:
            print("Error connection PLC. Error: ", e)
            continue

        # Set a runtime delay.
        time.sleep(plc_sleep)

"""
---------------------------------------
MAIN PROGRAM
---------------------------------------
"""
def main():
    """
    Main program.
    Start connection to the SQLITE3.
    Call 2 trheads running concurrently in an infinite loop.
        - read_plc()
        - write_sql().
    """
    # Create and start threats.
    read_plc_thread = Thread(target = read_plc)
    write_sql_thread = Timer(3, function = write_sql) # TODO: , args = (sql_connection, sql_cursor))
    read_plc_thread.start()
    write_sql_thread.start()

if __name__ == "__main__":
    print("RASPY-COM\n-----------")
    ao = OEE.OEE(10)
    print(" ----------------  ", ao.num_iterations)
    # main()
