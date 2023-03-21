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
from datetime import datetime, timedelta

class OEE():
    """
    Class OEE.
    Calculate the OEE since shift has started.
    This class has 3 subclasses: Availability, Quality and  Performance.
    The OEE is the product of «Availability», «Quality» and «Performance».
    """
    def __init__(self, interval_duration, cycle_time, sql_connection, sql_cursor):
        """
        Constructor.
        """
        self.sql_connection = sql_connection
        self.sql_cursor = sql_cursor
        self.interval_duration = interval_duration
        self.cycle_time = cycle_time
        self.break_time_interval_duration = 0
        self.num_iterations = 0
        self.num_maintenance = 0
        self.num_error = 0
        self.start_shift_time = '00:00:00'
        self.end_shift_time = '00:00:00'
        self.break_shift_time = 0

    def set_interval_duration(self, interval_duration):
        """
        Update interval duration.
        """
        self.interval_duration = interval_duration

    def set_cycle_time(self, cycle_time):
        """
        Update cycle time.
        """
        self.cycle_time = cycle_time

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
        self.sql_connection.commit()
        self.sql_connection.close()

    def get_break_shift_time(self):
        """
        Get the break time of the current shift.
        Break time will be 0 in some shifts.
        """
        # Select break time from current shift.
        sql_query = "SELECT Break_time FROM table_shifts WHERE days LIKE '%{}%' AND Start_time = '{}'".format(
            time.strftime("%A"), self.start_shift_time)
        try:
            self.sql_cursor.execute(sql_query)
            self.sql_connection.commit()
            result = self.sql_cursor.fetchone()[0]
            self.break_shift_time = result if result != None else 0
        except sqlite3.OperationalError as e:
            print("Error to get the end time of the shift. Error: ", e)
            return -1

        return 0

    def get_start_shift_time(self):
        """
        Get the start time of the current shift.
        The night shift has extended for 2 days (22:00 to 06:00), so it must be calculated differently.
        """
        # Get the current time.
        current_time = datetime.now().strftime("%H:%M:%S")

        # Select started hour from current shift.
        if (current_time >= '06:00:00' and current_time < '22:00:00'):
            sql_query = "SELECT Start_time FROM table_shifts WHERE days LIKE '%{}%' AND Start_time <= '{}' AND End_time > '{}'".format(
                time.strftime("%A"), current_time, current_time)

            try:
                self.sql_cursor.execute(sql_query)
                self.sql_connection.commit()
                self.start_shift_time = self.sql_cursor.fetchone()[0]
                # TODO result = self.sql_cursor.fetchone()[0]
                # TODO self.start_shift_time = result if result != None else 0

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
                self.start_shift_time = self.sql_cursor.fetchone()[0]
                # TODO result = self.sql_cursor.fetchone()[0]
                # TODO self.start_shift_time = result if result != None else 0

            except sqlite3.OperationalError as e:
                print("Error to get the start time of the shift. Error: ", e)
                return -1

        return 0

    def get_end_shift_time(self):
        """
        Get the end time of the current shift.
        The night shift has extended for 2 days (22:00 to 06:00), so it must be calculated differently.
        """
        # Get the current time.
        current_time = datetime.now().strftime("%H:%M:%S")

        # Select ending hour from current shift.
        if (current_time >= '06:00:00' and current_time < '22:00:00'):
            sql_query = "SELECT End_time FROM table_shifts WHERE days LIKE '%{}%' AND Start_time <= '{}' AND End_time > '{}'".format(
                time.strftime("%A"), current_time, current_time)
            try:
                self.sql_cursor.execute(sql_query)
                self.sql_connection.commit()
                self.end_shift_time = self.sql_cursor.fetchone()[0]
                # TODO result = self.sql_cursor.fetchone()[0]
                # TODO self.start_shift_time = result if result != None else 0
            except sqlite3.OperationalError as e:
                print("Error to get the end time of the shift. Error: ", e)
                return -1

        # If the current time is < 6AM or > 10PM, the current shift is night.
        # It externds for 2 days, so it's calcualted differently.
        else:
            sql_query = "SELECT MIN(End_time) FROM table_shifts WHERE days LIKE '%{}%'".format(time.strftime("%A"))
            try:
                self.sql_cursor.execute(sql_query)
                self.sql_connection.commit()
                self.end_shift_time = self.sql_cursor.fetchone()[0]
                # TODO result = self.sql_cursor.fetchone()[0]
                # TODO self.start_shift_time = result if result != None else 0
            except sqlite3.OperationalError as e:
                print("Error to get the end time of the shift. Error: ", e)
                return -1

        return 0

    """
    ---------------------------------------
    OVERALL EQUIPMENT EFFECTIVENESS
    ---------------------------------------
    """
    def get_oee(self):
        """
        Get the Overall Equipment Efectiveness since shift started.
        OEE is the product of «Availability», «Performance» and «Quality».
        """
        return (100 * self.get_availability()/100 * self.get_performance()/100 * self.get_quality()/100)

    """
    ---------------------------------------
    AVAILABILITY
    ---------------------------------------
    """
    def get_availability(self):
        """
        Get the «AVAILABILITY» parameter for the OEE calculation.
        """
        if ((self.work_time() - self.planned_stops_time()) == 0):
                print("TPO (Total work time - tota break time planned) is 0. Number divided by 0 is infinity.")
                return 0

        return round((100 * (self.work_time() - self.planned_stops_time() - self.error_time()) /
                     (self.work_time() - self.planned_stops_time())), 2)

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
        if (self.total_time_shift() == 0):
            print("Total time shift is 0. Number divided by 0 is infinity.")
            return 0

        return (self.break_shift_time * 60 * self.interval_duration / self.total_time_shift())

    def total_time_shift(self):
        """
        Get the total time shift.
        end_shift_hour - start_shift_hour
        """
        if (self.end_shift_time == None ) or (self.start_shift_time == None):
            print("The total shift time is NONE.")
            return 0

        return (datetime.strptime(self.end_shift_time, '%H:%M:%S') -
                datetime.strptime(self.start_shift_time, "%H:%M:%S")).seconds

    def error_time(self):
        """
        Get the toal erros time in the current shift.
        num_error * interval.
        """
        return (self.num_error * self.interval_duration)

    """
    ---------------------------------------
    PERFORMANCE
    ---------------------------------------
    """
    def get_performance(self):
        """
        Get the «PERFORMANCE» parameter for the OEE calculation.
        The performance parameter is the result of dividing the total pieces fabricated in an interval of time
        by the pieces that theoretically could have been produced in the same time.
        """
        if ((self.cycle_time * self.work_time()) == 0):
            print("Indefined work get performance. Number divided by 0 is infinty.")
            return 0

        return round((100 * self.total_pieces_fabricated() / (self.cycle_time * self.work_time())), 2)

    """
    ---------------------------------------
    QUALITY
    ---------------------------------------
    """
    def get_quality(self):
        """
        Get the «QUALITY» parameter for the OEE calculation.
        The quality parameter is the total of pieces correctly fabricated (OK) divided
        by total of pieces fabricated (OK + NOK).
        """
        if (self.total_pieces_fabricated() == 0):
            print("No pieces fabricated since current shift started. Number divided by 0 is infinty.")
            return 0

        return round((100 * self.total_pieces_ok_fabricated() / self.total_pieces_fabricated()), 2)

    def total_pieces_ok_fabricated(self):
        """
        Select from «table_plc» of the database the total pieces fabricated correctly (OK).
        The night shift has extended for 2 days (22:00 to 06:00), so it must be calculated differently.
        """
        # Get the current time.
        current_time = datetime.now().strftime("%H:%M:%S")

        # Select all pieces fabricated for current shift.
        if (current_time >= '06:00:00' and current_time < '22:00:00'):
            sql_query = "SELECT SUM(OK) FROM table_plc WHERE Date = '{}' AND Hour >= '{}' AND Hour < '{}' AND Rework = 'False'".format(
                datetime.today().strftime("%D"), self.start_shift_time, self.end_shift_time)

            try:
                self.sql_cursor.execute(sql_query)
                self.sql_connection.commit()
                result = self.sql_cursor.fetchone()[0]
            except sqlite3.OperationalError as e:
                print("Error to count all pieces from the DB: ", e)
                return -1

        # If the current time is < 6AM or > 10PM, the current shift is night.
        # It extends for 2 days, so it's calculated differently.
        else:
            sql_query = "SELECT SUM(OK) FROM table_plc WHERE (Date = '{}' AND Hour >= '{}') OR (Date = '{}' AND Hour < '{}')".format(
                (datetime.today() - timedelta(days = 1)).strftime("%D"), self.start_shift_time,
                datetime.today().strftime("%D"), self.end_shift_time)

            try:
                self.sql_cursor.execute(sql_query)
                self.sql_connection.commit()
                result = self.sql_cursor.fetchone()[0]
            except sqlite3.OperationalError as e:
                print("Error to count all pieces from the DB: ", e)
                return -1

        return result if result != None else 0

    """
    ---------------------------------------
    COMMON FUNCTIONS
    ---------------------------------------
    """
    def work_time(self):
        """
        Get the total work time since current shift has started.
        """
        return (self.num_iterations * self.interval_duration)

    def total_pieces_fabricated(self):
        """
        Select from «table_plc» of the database the total pieces fabricted (OK + NOK).
        The night shift has extended for 2 days (22:00 to 06:00), so it must be calculated differently.
        """
        # Get the current time.
        current_time = datetime.now().strftime("%H:%M:%S")

        # Select all pieces fabricated for current shift.
        if (current_time >= '06:00:00' and current_time < '22:00:00'):
            sql_query = "SELECT SUM(OK + NOK) FROM table_plc WHERE Date = '{}' AND Hour >= '{}' AND Hour < '{}'".format(
                datetime.today().strftime("%D"), self.start_shift_time, self.end_shift_time)

            try:
                self.sql_cursor.execute(sql_query)
                self.sql_connection.commit()
                result = self.sql_cursor.fetchone()[0]
            except sqlite3.OperationalError as e:
                print("Error to count all pieces from the DB: ", e)
                return -1

        # If the current time is < 6AM or > 10PM, the current shift is night.
        # It extends for 2 days, so it's calculated differently.
        else:
            sql_query = "SELECT SUM(OK + NOK) FROM table_plc WHERE (Date = '{}' AND Hour >= '{}') OR (Date = '{}' AND Hour < '{}')".format(
                (datetime.today() - timedelta(days = 1)).strftime("%D"), self.start_shift_time,
                datetime.today().strftime("%D"), self.end_shift_time)

            try:
                self.sql_cursor.execute(sql_query)
                self.sql_connection.commit()
                result = self.sql_cursor.fetchone()[0]
            except sqlite3.OperationalError as e:
                print("Error to count all pieces from the DB: ", e)
                return -1

        return result if result != None else 0

if __name__ == '__main__':
    # Start connection.
    sql_path = "/media/rpiiot/CCCOMA_X64F/4246_IOT.db"
    sql_connection = sqlite3.connect(sql_path)
    sql_cursor = sql_connection.cursor()

    # Class OEE.
    current_oee = OEE(10, 10, sql_connection, sql_cursor)
    # sql_connection.close()

    print("---------------------------------")
    print("OEE VALUES\n---------------------------------")
    print("\tInterval duration: ", current_oee.interval_duration)
    print("\tCycle time: ", current_oee.cycle_time)
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

    print("---------------------------------")
    print("RESET BEFORE\n---------------------------------")
    print("\tInterval duration: ", current_oee.interval_duration)
    print("\tCycle time: ", current_oee.cycle_time)
    print("\tNum iterations: ", current_oee.num_iterations)
    print("\tNum maintenances: ", current_oee.num_maintenance)
    print("\tNum errors: ", current_oee.num_error)
    print("\tStart shift hour: ", current_oee.start_shift_time)
    print("\tEnd shift hour: ", current_oee.end_shift_time)
    print("\tBreak shift hour: ", current_oee.break_shift_time)

    current_oee.reset_values()

    print("---------------------------------")
    print("RESET AFTER\n---------------------------------")
    print("\tInterval duration: ", current_oee.interval_duration)
    print("\tCycle time: ", current_oee.cycle_time)
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

    print("---------------------------------")
    print("OEE VALUES\n---------------------------------")
    print("\tInterval duration: ", current_oee.interval_duration)
    print("\tCycle time: ", current_oee.cycle_time)
    print("\tNum iterations: ", current_oee.num_iterations)
    print("\tNum maintenances: ", current_oee.num_maintenance)
    print("\tNum errors: ", current_oee.num_error)
    print("\tStart shift hour: ", current_oee.start_shift_time)
    print("\tEnd shift hour: ", current_oee.end_shift_time)
    print("\tBreak shift hour: ", current_oee.break_shift_time)

    print("...........................")
    print("AVAILABILITY\n...........................")
    print("\tTotal shift time (End hour shift - Start hour shift): ", current_oee.total_time_shift())
    print("\tTotal work time: ", current_oee.work_time())
    print("\tPlanned stops time: ", current_oee.planned_stops_time())
    print("\tError time: ", current_oee.error_time())
    print("\tAvailability: ", current_oee.get_availability())

    print("...........................")
    print("PERFORMANCE\n...........................")
    print("\tTotal pieces fabricated (OK + NOK): ", current_oee.total_pieces_fabricated())
    print("\tCycle time: ", current_oee.cycle_time)
    print("\tTotal work time: ", current_oee.work_time())
    print("\tPerformance: ", current_oee.get_performance())

    print("...........................")
    print("QUALITY\n...........................")
    print("\tTotal pieces correctly fabricated (OK): ", current_oee.total_pieces_fabricated())
    print("\tTotal pieces fabricated (OK + NOK): ", current_oee.total_pieces_fabricated())
    print("\tQuality: ", current_oee.get_quality())

    print("...........................")
    print("Overall Equipment Effectiveness\n...........................")
    print("\tAvailability: ", current_oee.get_availability())
    print("\tPerformance: ", current_oee.get_performance())
    print("\tQuality: ", current_oee.get_quality())
    print("\tOEE: ", current_oee.get_oee())

    # Close connection
    current_oee.close_connection()
    sql_connection.close()