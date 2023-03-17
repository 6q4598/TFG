#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import sqlite3
import snap7
from snap7 import util
from datetime import datetime, timedelta
from threading import *

db_values = {'Auto': 0, 'Man': 0, 'Auditoria': 0, 'Error': 0, 'Ok': 0, 'Nok': 0, 'Error': []}
fabricated = False
num_ok = num_nok = 0
sql_path = "/media/rpiiot/CCCOMA_X64F/4246_IOT.db"

# The night shift extends for two days.
two_days_shift = False
interval = 10

def get_count_intervals_total_shift(h, hh):
    """
    Function that returns the total number of shifts has a turn.
    The number of shifts in a turn is the total time duration shift (final hour - start hour) divided by the interval duration.
    """
    print(type(h), " --- ", h);
    print(type(hh), " --- ", hh);
    return 0
    # return str(datetime.strptime(hh, '%H:%M:%S') - datetime.strptime(h, '%H:%M:%S'))

def get_total_time(sql_connection, sql_cursor, k):
    """
    Function that return the total time that has passed since the
    current turn started.
    """
    return interval * k

def get_count_intervals_shift(sql_connection, sql_cursor, h, hh):
    """
    Function that returns the number of time intervals since
    the current shift started.
    """
    #############################################################
    # TODO:
    # Ficar els paràmetres «h» i «hh» dins la funció.
    # «h» és el temps inicial del torn.
    # «hh» és el temps final del torn.
    #############################################################
    if (h >= '06:00:00' and h < '22:00:00'):
        sql_query = "SELECT COUNT(*) FROM table_plc WHERE Date = '{}' AND Hour >= '{}' AND Hour < '{}'".format(time.strftime("%D"), h, hh)
        try:
            sql_cursor.execute(sql_query)
            sql_connection.commit()
            return sql_cursor.fetchone()[0]
        except sqlite3.OperationalError as e:
            print("Error to get the start time of the shift. Error: ", e)
            return -1
    sql_query = "SELECT COUNT(*) FROM table_plc  WHERE (Date = '{}' AND Hour >= '{}') OR (Date = '{}' AND Hour  < '{}')".format(
        (datetime.now() - timedelta(days=1)).strftime("%D"), h, time.strftime("%D"), hh)
    try:
        sql_cursor.execute(sql_query)
        sql_connection.commit()
        return sql_cursor.fetchone()[0]
    except sqlite3.OperationalError as e:
        print("Error to get the start time of the shift. Error: ", e)
        return -1

def get_start_shift_hour(sql_connection, sql_cursor, h):
    """
    Function that returns the start hour of the current shift.
    Current shift is determine dy the day of the week and the time we are in.
    """
    if (h >= '06:00:00' and h < '22:00:00'):
        sql_query = "SELECT Start_time FROM table_shifts WHERE days LIKE '%{}%' AND Start_time < '{}' AND End_time > '{}'".format(
            time.strftime("%A"), h, h
        )
        try:
            sql_cursor.execute(sql_query)
            sql_connection.commit()
            return sql_cursor.fetchone()[0]
        except sqlite3.OperationalError as e:
            print("Error to get the start time of the shift. Error: ", e)
            return -1
    sql_query = "SELECT MAX(Start_time) FROM table_shifts WHERE days LIKE '%{}%'".format(time.strftime("%A"))
    try:
        sql_cursor.execute(sql_query)
        sql_connection.commit()
        return sql_cursor.fetchone()[0]
    except sqlite3.OperationalError as e:
        print("Error to get the start time of the shift. Error: ", e)
        return -1

def get_end_shift_hour(sql_connection, sql_cursor, h):
    """
    Function that returns the start hour of the current shift.
    Current shift is determine dy the day of the week and the time we are in.
    """
    if (h >= '06:00:00' and h < '22:00:00'):
        sql_query = "SELECT End_time FROM table_shifts WHERE days LIKE '%{}%' AND Start_time < '{}' AND End_time > '{}'".format(
            time.strftime("%A"), h, h
        )
        try:
            sql_cursor.execute(sql_query)
            sql_connection.commit()
            return sql_cursor.fetchone()[0]
        except sqlite3.OperationalError as e:
            print("Error to get the start time of the shift. Error: ", e)
            return -1
    sql_query = "SELECT Min(End_time) FROM table_shifts WHERE days LIKE '%{}%'".format(time.strftime("%A"))
    try:
        sql_cursor.execute(sql_query)
        sql_connection.commit()
        return sql_cursor.fetchone()[0]
    except sqlite3.OperationalError as e:
        print("Error to get the start time of the shift. Error: ", e)
        return -1

sql_connection = sqlite3.connect(sql_path)
sql_cursor = sql_connection.cursor()
print(get_count_intervals_total_shift(get_start_shift_hour(sql_connection, sql_cursor, '01:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '01:00:00')))
print(get_count_intervals_total_shift(get_start_shift_hour(sql_connection, sql_cursor, '21:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '21:00:00')))
print(get_count_intervals_total_shift(get_start_shift_hour(sql_connection, sql_cursor, '11:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '11:00:00')))
print(get_count_intervals_total_shift(get_start_shift_hour(sql_connection, sql_cursor, '15:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '15:00:00')))
print(get_count_intervals_total_shift(get_start_shift_hour(sql_connection, sql_cursor, '00:01:00'), get_end_shift_hour(sql_connection, sql_cursor, '00:01:00')))
print(get_count_intervals_total_shift(get_start_shift_hour(sql_connection, sql_cursor, '23:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '23:00:00')))
print(get_count_intervals_total_shift(get_start_shift_hour(sql_connection, sql_cursor, '13:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '13:00:00')))
print(get_count_intervals_total_shift(get_start_shift_hour(sql_connection, sql_cursor, '20:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '20:00:00')))
sql_connection.close()

"""
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor, get_start_shift_hour(sql_connection, sql_cursor, '01:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '01:00:00'))))
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor, get_start_shift_hour(sql_connection, sql_cursor, '21:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '21:00:00'))))
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor, get_start_shift_hour(sql_connection, sql_cursor, '11:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '11:00:00'))))
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor, get_start_shift_hour(sql_connection, sql_cursor, '15:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '15:00:00'))))
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor, get_start_shift_hour(sql_connection, sql_cursor, '00:01:00'), get_end_shift_hour(sql_connection, sql_cursor, '00:01:00'))))
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor, get_start_shift_hour(sql_connection, sql_cursor, '23:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '23:00:00'))))
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor, get_start_shift_hour(sql_connection, sql_cursor, '13:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '13:00:00'))))

print(get_count_intervals_shift(sql_connection, sql_cursor, get_start_shift_hour(sql_connection, sql_cursor, '20:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '20:00:00'))))

print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor, get_start_shift_hour(sql_connection, sql_cursor, '20:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '20:00:00'))))

"""

"""
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor,get_start_shift_hour(sql_connection, sql_cursor, '01:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '01:00:00'))))
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor,get_start_shift_hour(sql_connection, sql_cursor, '21:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '21:00:00'))))
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor,get_start_shift_hour(sql_connection, sql_cursor, '11:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '11:00:00'))))
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor,get_start_shift_hour(sql_connection, sql_cursor, '15:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '15:00:00'))))
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor,get_start_shift_hour(sql_connection, sql_cursor, '00:01:00'), get_end_shift_hour(sql_connection, sql_cursor, '00:01:00'))))
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor,get_start_shift_hour(sql_connection, sql_cursor, '23:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '23:00:00'))))
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor,get_start_shift_hour(sql_connection, sql_cursor, '13:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '13:00:00'))))
print(get_total_time(sql_connection, sql_cursor, get_count_intervals_shift(sql_connection, sql_cursor,get_start_shift_hour(sql_connection, sql_cursor, '20:00:00'), get_end_shift_hour(sql_connection, sql_cursor, '20:00:00'))))
"""
