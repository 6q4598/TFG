#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import snap7
import sqlite3
import os
import datetime
from snap7 import util
from threading import *

class OEE():
    """
    Class OEE.
    Calculate the OEE since shift has started.
    This class has 3 subclasses: Availability, Quality and  Performance.
    The OEE is the product of «Availability», «Quality» and «Performance».
    """
    def __init__(self, interval_duration, sql_connection, sql_cursor):
        # TODO TODO TODO
        # Arreglar els SQL_CONNECTION i els SQL_CURSOR.
        # TODO TODO TODO
        """
        Constructor.
        """
        self.sql_connection = sql_connection
        self.sql_cursor = sql_cursor
        self.interval_duration = interval_duration
        self.break_time_interval_duration = 0
        self.num_iterations = 0
        self.num_maintenance = 0
        self.num_error = 0
        self.start_shift_time = '00:00:00'
        self.end_shift_time = '00:00:00'
        self.break_shift_time = 0

    def sum_iteration(self):
        """
        Sum inserts in the database.
        """
        self.num_iterations += 1

    def sum_maintenance(self):
        """
        Sum maintenance inserts in the database.
        """
        self.num_maintenance += 1

    def sum_error(self):
        """
        Sum error inserts in the database.
        """
        self.num_error += 1

    def reset_values(self):
        """
        Reset values because shift has changed.
        """
        self.break_time_interval_duration = 0
        self.num_iterations = 0
        self.num_maintenance = 0
        self.num_error = 0
        self.start_shift_time = '00:00:00'
        self.end_shift_time = '00:00:00'
        self.break_shift_time = 0

    def close_connection(self):
        """
        Close database connection.
        """
        self.sql_connection.close()

    def get_break_shift_time(self):
        """
        Get the break time of the current shift.
        """
        # Select ending hour from current shift.
        sql_query = "SELECT Break_time FROM table_shifts WHERE days LIKE '%{}%' AND Start_time = '{}'".format(
            time.strftime("%A"), self.start_shift_time)
        try:
            self.sql_cursor.execute(sql_query)
            self.sql_connection.commit()
            self.break_shift_time = self.sql_cursor.fetchone()[0]
        except sqlite3.OperationalError as e:
            print("Error to get the end time of the shift. Error: ", e)
            return -1
        return 0

    def get_start_shift_time(self):
        """
        Get the start time of the current shift.
        """
        # Get the current time.
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        # Select started hour from current shift.
        if (current_time >= '06:00:00' and current_time < '22:00:00'):
            sql_query = "SELECT Start_time FROM table_shifts WHERE days LIKE '%{}%' AND Start_time <= '{}' AND End_time > '{}'".format(
                time.strftime("%A"), current_time, current_time)

            try:
                self.sql_cursor.execute(sql_query)
                self.sql_connection.commit()
                # If the start shift time of current shift is different to start
                # shift time stored, reset values because shift changed.
                # Donar-li una volta.
                # TODO - st = self.sql_cursor.fetchone()[0]
                # TODO - if (self.start_shift_time != st):
                # TODO -     self.reset_values()
                self.start_shift_time = self.sql_cursor.fetchone()[0]

            except sqlite3.OperationalError as e:
                print("Error to get the start time of the shift. Error: ", e)
                return -1

        # If the current time is < 6AM or > 10PM, the current shift is night.
        # It externds for 2 days, so it0s calcualted differently.
        else:
            sql_query = "SELECT MAX(Start_time) FROM table_shifts WHERE days LIKE '%{}%'".format(time.strftime("%A"))

            try:
                self.sql_cursor.execute(sql_query)
                self.sql_connection.commit()
                # TODO - st = self.sql_cursor.fetchone()[0]
                # TODO - if (self.start_shift_time != st):
                # TODO -     self.reset_values()
                self.start_shift_time = self.sql_cursor.fetchone()[0]

            except sqlite3.OperationalError as e:
                print("Error to get the start time of the shift. Error: ", e)
                return -1

    def get_end_shift_time(self):
        """
        Get the end time of the current shift.
        """
        # Get the current time.
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        # Select ending hour from current shift.
        if (current_time >= '06:00:00' and current_time < '22:00:00'):
            sql_query = "SELECT End_time FROM table_shifts WHERE days LIKE '%{}%' AND Start_time <= '{}' AND End_time > '{}'".format(
                time.strftime("%A"), current_time, current_time)
            try:
                self.sql_cursor.execute(sql_query)
                self.sql_connection.commit()
                self.end_shift_time = self.sql_cursor.fetchone()[0]
            except sqlite3.OperationalError as e:
                print("Error to get the end time of the shift. Error: ", e)
                return -1

        # If the current time is < 6AM or > 10PM, the current shift is night.
        # It externds for 2 days, so it0s calcualted differently.
        else:
            sql_query = "SELECT MIN(End_time) FROM table_shifts WHERE days LIKE '%{}%'".format(time.strftime("%A"))
            try:
                self.sql_cursor.execute(sql_query)
                self.sql_connection.commit()
                self.end_shift_time = self.sql_cursor.fetchone()[0]
            except sqlite3.OperationalError as e:
                print("Error to get the end time of the shift. Error: ", e)
                return -1

    """
    ---------------------------------------
    AVAILABILITY
    ---------------------------------------
    """
    def get_availability(self):
        """
        Get the «AVAILABILITY» parameter for the OEE calculation.
        """
        return (100 * (self.work_time() - self.planned_stops_time() - self.error_time()) /
        (self.work_time() - self.planned_stops_time()))

    def work_time(self):
        """
        Get the total work time since current shift has started.
        """
        return (self.num_iterations * self.interval_duration)

    def planned_stops_time(self):
        """
        Get the planned stops since current shift has started.
        Is calculated by the following formula:
        (num_iteration * break_time_interval) + (num_maintenance * interval_duration)
        """
        return (self.num_iterations * self.break_time_interval()) + (self.num_maintenance * self.interval_duration)

    def break_time_interval(self):
        """
        Get break time by interval.
        We needs converts total_time_break_shift (in minutes) to seconds.
        (total_time_break_shift * interval_duration) / (total_time_shift)
        total_time_shift can be different depending on the shift.
        """
        return (((self.break_shift_time * 60) * self.interval_duration) / (self.total_time_shift()))

    def total_time_shift(self):
        """
        Get the total time shift.
        end_shift_hour - start_shift_hour
        """
        return (datetime.datetime.strptime(self.end_shift_time, '%H:%M:%S') -
                datetime.datetime.strptime(self.start_shift_time, "%H:%M:%S")).seconds

    def error_time(self):
        """
        Get the toal erros time in the current shift.
        num_error * interval.
        """
        return (self.num_error * self.interval_duration)

    """
    ---------------------------------------
    QUALITY
    ---------------------------------------
    """

    """
    ---------------------------------------
    PERFORMANCE
    ---------------------------------------
    """

class Availability(OEE):
    """
    Subclass «availability».
    Calculates the availability parameter for calculating the OEE.
    """
    pass

class Quality(OEE):
    """
    Subclass «Quality».
    Calculates the quality parameter for calculating the OEE.
    """
    pass

class Performance(OEE):
    """
    Subclass «Performance».
    Calculates the performance parameter for calculating the OEE.
    """
    pass

if __name__ == '__main__':
    # Start connection.
    sql_path = "/media/rpiiot/CCCOMA_X64F/4246_IOT.db"
    sql_connection = sqlite3.connect(sql_path)
    sql_cursor = sql_connection.cursor()

    # Class OEE.
    current_oee = OEE(10, sql_connection, sql_cursor)
    # sql_connection.close()

    print("OEE VALUES\n---------------------------------")
    print("\tNum iterations: ", current_oee.num_iterations)
    print("\tNum maintenances: ", current_oee.num_maintenance)
    print("\tNum errors: ", current_oee.num_error)
    print("\tStart shift hour: ", current_oee.start_shift_time)
    print("\tEnd shift hour: ", current_oee.end_shift_time)
    print("\tBreak shift hour: ", current_oee.break_shift_time)

    # Insert virtual values.
    for k in range(100):
        current_oee.sum_iteration()

    for k in range(20):
        current_oee.sum_maintenance()

    for k in range(10):
        current_oee.sum_error()

    # Get current shift hours.
    current_oee.get_start_shift_time()
    current_oee.get_end_shift_time()
    current_oee.get_break_shift_time()

    print("OEE VALUES\n---------------------------------")
    print("\tNum iterations: ", current_oee.num_iterations)
    print("\tNum maintenances: ", current_oee.num_maintenance)
    print("\tNum errors: ", current_oee.num_error)
    print("\tStart shift hour: ", current_oee.start_shift_time)
    print("\tEnd shift hour: ", current_oee.end_shift_time)
    print("\tBreak shift hour: ", current_oee.break_shift_time)

    print("AVAILABILITY\n... ... ... ... ... ... ...")
    print("\tTotal shift time (End hour shift - Start hour shift): ", current_oee.total_time_shift())
    print("\tTotal work time: ", current_oee.work_time())
    print("\tPlanned stops time: ", current_oee.planned_stops_time())
    print("\tError time: ", current_oee.error_time())
    print("\tAvailability: ", current_oee.get_availability())

    """
    obc = OEE(10, sql_connection, sql_cursor)
    print(obc.num_iterations)
    print(obc.start_shift_time)
    print(obc.end_shift_time)
    print(obc.break_shift_time)

    obc.sum_iteration()
    obc.get_start_shift_time()
    obc.end_shift_hour()
    print(obc.num_iterations)
    print(obc.start_shift_time)
    print(obc.end_shift_time)
    print("--")
    print(obc.start_shift_time)
    print(type(obc.end_shift_time))
    print("--")
    print(type(obc.end_shift_time))
    print("--")
    secshift = obc.total_time_shift()
    print(secshift)
    obc.get_break_shift_time()
    aaa = obc.break_shift_time;
    print(aaa)
    print("--- ", type(aaa))
    """

    # Close connection
    sql_connection.close()
    current_oee.close_connection()
