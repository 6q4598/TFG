#!/usr/bin/env pythongT
# -*- coding: utf-8 -*-

import sys
import time
import snap7
import sqlite3
import os
import datetime
from db import db
from snap7 import util
from threading import *
from datetime import datetime, timedelta

class oee():
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
        self.object_db = db()
        # ---------------------------------
        self.start_shift_time = '00:00:00'
        self.end_shift_time = '00:00:00'
        self.break_time = '00:00:00'
        self.break_duration = 0
        self.maintenance_time = '00:00:00'
        self.maintenance_duration = 0
        # ---------------------------------
        self.availability = 0
        self.performance = 0
        self.quality = 0
        self.oee = 0
        # ---------------------------------
        self.current_work_time = 0
        self.current_planned_stop_time = 0
        self.current_error_time = 0

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

    def reset_values(self):
        """
        Reset values because shift has changed.
        """
        self.start_shift_time = '00:00:00'
        self.end_shift_time = '00:00:00'
        self.break_time = '00:00:00'
        self.break_duration = 0
        self.maintenance_time = 0
        self.maintenance_duration = 0
        # ---------------------------------
        self.availability = 0
        self.performance = 0
        self.quality = 0
        # ---------------------------------
        self.current_work_time = 0
        self.current_planned_stop_time= 0
        self.current_error_time = 0

    def close_connection(self):
        """
        Close database connection.
        """
        self.sql_connection.commit()
        self.sql_connection.close()

    def get_num_iterations(self):
        """
        Get the registers writted to the database since current shift has started.
        """
        current_time = datetime.now().strftime("%H:%M:%S")
        if (current_time >= "06:00" and current_time < "22:00:00"):
            sql_query = "SELECT COUNT(*) FROM table_plc WHERE Date = '{}' AND Hour >= '{}' AND Hour < '{}'".format(
                time.strftime("%D"), self.start_shift_time, self.end_shift_time)
        elif (current_time > "22:00:00"):
            sql_query = "SELECT COUNT(*) FROM table_plc WHERE (Date = '{}' AND Hour >= '{}')".format(
                time.strftime("%D"), self.start_shift_time)
        else:
            sql_query = "SELECT COUNT(*) FROM table_plc WHERE (Date = '{}' AND Hour >= '{}') OR (Date = '{}' AND Hour < '{}')".format(
                (datetime.today() - timedelta(days = 1)).strftime("%D"), self.start_shift_time,
                time.strftime("%D"), self.end_shift_time)
        result = self.object_db.write_to_db(self.sql_connection, self.sql_cursor, sql_query)
        return result if (result >= 0 or result != None) else 0

    def get_break_time(self):
        """
        Get the start break time of the current shift.
        """
        sql_query = "SELECT Break_time FROM table_shifts WHERE days LIKE '%{}%' AND Start_time = '{}'".format(
            time.strftime("%A"), self.start_shift_time)
        result = self.object_db.write_to_db(self.sql_connection, self.sql_cursor, sql_query)
        self.break_time = result # if result != -1 else "None"
        return self.break_time

    def get_break_duration(self):
        """
        Get the break time of the current shift.
        Break time will be 0 in some shifts.
        """
        # Select break time from current shift.
        sql_query = "SELECT Break_duration FROM table_shifts WHERE days LIKE '%{}%' AND Start_time = '{}'".format(
            time.strftime("%A"), self.start_shift_time)
        result =  self.object_db.write_to_db(self.sql_connection, self.sql_cursor, sql_query)
        self.break_duration = result #  if result >= 0 or result != None else 0
        return self.break_time

    def get_maintenance_time(self):
        """
        Get the start break time of the current shift.
        """
        sql_query = "SELECT Maintenance_time FROM table_shifts WHERE days LIKE '%{}%' AND Start_time = '{}'".format(
            time.strftime("%A"), self.start_shift_time)
        result = self.object_db.write_to_db(self.sql_connection, self.sql_cursor, sql_query)
        self.maintenance_time = result # if result != -1 else "None"
        return self.maintenance_time

    def get_maintenance_duration(self):
        """
        Get the break time of the current shift.
        Break time will be 0 in some shifts.
        """
        # Select break time from current shift.
        sql_query = "SELECT Maintenance_duration FROM table_shifts WHERE days LIKE '%{}%' AND Start_time = '{}'".format(
            time.strftime("%A"), self.start_shift_time)
        result =  self.object_db.write_to_db(self.sql_connection, self.sql_cursor, sql_query)
        self.maintenance_duration = result # if result >= 0 or result != None else 0
        return self.maintenance_duration

    def get_start_shift_time(self):
        """
        Get the start time of the current shift.
        The night shift has extended for 2 days (22:00 to 06:00), so it must be calculated differently.
        If the current time is < 6AM or > 10PM, the current shift is night.
        It externds for 2 days, so it's calcualted differently.
        """
        current_time = datetime.now().strftime("%H:%M:%S")

        # Select started hour from current shift.
        if (time.strftime("%A") == "Saturday" and current_time < "06:00:00"):
            sql_query = "SELECT MAX(Start_time) FROM table_shifts WHERE days LIKE '%Friday%'";
        elif (current_time >= '06:00:00' and current_time < '22:00:00'):
            sql_query = "SELECT Start_time FROM table_shifts WHERE days LIKE '%{}%' AND Start_time <= '{}' AND End_time > '{}'".format(
                time.strftime("%A"), current_time, current_time)
        else:
            sql_query = "SELECT MAX(Start_time) FROM table_shifts WHERE days LIKE '%{}%'".format(time.strftime("%A"))

        result = self.object_db.write_to_db(self.sql_connection, self.sql_cursor, sql_query)
        if (result != None and result != -1):
            self.start_shift_time = result
        return result

    def get_end_shift_time(self):
        """
        Get the end time of the current shift.
        The night shift has extended for 2 days (22:00 to 06:00), so it must be calculated differently.
        If the current time is < 6AM or > 10PM, the current shift is night.
        """
        current_time = datetime.now().strftime("%H:%M:%S")

        if (time.strftime("%A") == "Saturday" and current_time < "06:00:00"):
            sql_query = "SELECT MIN(Start_time) FROM table_shifts WHERE days LIKE '%Saturday%'";
        elif (current_time >= '06:00:00' and current_time < '22:00:00'):
            sql_query = "SELECT End_time FROM table_shifts WHERE Days LIKE '%{}%' AND Start_time <= '{}' AND End_time > '{}'".format(
                time.strftime("%A"), current_time, current_time)
        else:
            sql_query = "SELECT MIN(End_time) FROM table_shifts WHERE days LIKE '%{}%'".format(time.strftime("%A"))

        result = self.object_db.write_to_db(self.sql_connection, self.sql_cursor, sql_query)
        if (result != None and result != -1):
            self.end_shift_time = result
        return result

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
        self.oee = round(((self.availability * self.performance * self.quality) / 100000), 2)
        if (self.oee < 0): self.oee = 0
        elif (self.oee > 100): self.oee = 100
        return self.oee

    """
    ---------------------------------------
    AVAILABILITY
    ---------------------------------------
    """
    def get_availability(self):
        """
        Get the «AVAILABILITY» parameter for the OEE calculation.
        """
        try:
            self.availability = round((100 * (self.current_work_time - self.current_planned_stop_time - self.current_error_time) / (self.current_work_time - self.current_planned_stop_time)), 2)

        except ZeroDivisionError:
            self.availability = 0

        if (self.availability < 0): self.availability = 0
        elif (self.availability > 100): self.availability = 100

        return self.availability

    def work_time(self):
        """
        Get the total work time since current shift has started.
        """
        current_time = datetime.now().strftime("%H:%M:%S")
        self.current_work_time = ((datetime.strptime(current_time, '%H:%M:%S') - datetime.strptime(self.start_shift_time, "%H:%M:%S")).seconds)
        return self.current_work_time

    def planned_stops_time(self):
        """
        Get the planned stops since current shift has started.
        Is calculated by the following formula:
        (num_iteration * break_time_interval) + (num_maintenance * interval_duration)
        """
        current_time = datetime.now().strftime("%H:%M:%S")

        # TODO - configure according to the requirements and the shifts of the client.
        if (current_time < "22:00.00"):

            # We consider whether the planned stops coincide in time with the planned maitenance.
            if ((self.break_time != -1) and (current_time >= self.break_time) and (self.break_duration > -1) and
                    (self.maintenance_time != -1) and (current_time >= self.maintenance_time) and (self.maintenance_duration > -1)):
                self.update_break_true()
                self.current_planned_stop_time += self.interval_duration;
                self.maintenance_duration -= 1
                self.break_duration -= 1

            elif (self.break_time != -1 and current_time >= self.break_time and self.break_duration > -1):
                self.update_break_true()
                self.current_planned_stop_time += self.interval_duration;
                self.break_duration -= 1

            elif (self.maintenance_time != -1 and current_time >= self.maintenance_time and self.maintenance_duration > -1):
                self.update_break_true()
                self.current_planned_stop_time += self.interval_duration;
                self.maintenance_duration -= 1

        return self.current_planned_stop_time

    def update_break_true(self):
        """
        Update table_plc last register.
        We consider wheteher the planned stops coincide in time with the planned maintenance.
        """
        sql_query = "UPDATE table_plc SET Break = True WHERE id = (SELECT id FROM table_plc ORDER BY id DESC LIMIT 1)"
        return self.object_db.write_to_db(self.sql_connection, self.sql_cursor, sql_query)

    def error_time(self):
        """
        Get the toal erros time in the current shift.
        num_error * interval.
        """
        self.current_error_time = (self.get_num_error() * self.interval_duration)
        return self.current_error_time

    def get_num_error(self):
        """
        Get total errors are in the database since current shift has started."
        """
        current_time = datetime.now().strftime("%H:%M:%S")

        if ('06:00:00' <= current_time < '22:00:00'):
            sql_query = "SELECT COUNT(*) FROM table_plc WHERE Date = '{}' AND Hour >= '{}' AND Hour < '{}' AND Error = 1 AND Break = FALSE".format(
                time.strftime("%D"), self.start_shift_time, self.end_shift_time)

        # If the current time is >= 22:00, the shift is night but the next day hasn't started yet.
        elif (current_time >= "22:00:00"):
            sql_query = "SELECT COUNT(*) FROM table_plc WHERE (Date = '{}' AND Hour >= '{}') AND Error = 1 AND Break = FALSE".format(
                time.strftime("%D"), self.start_shift_time)

        else:
            sql_query = "SELECT COUNT(*) FROM table_plc WHERE ((Date = '{}' AND Hour >= '{}') OR (Date = '{}' AND Hour < '{}')) AND Error = 1 AND Break = FALSE".format(
                (datetime.today() - timedelta(days = 1)).strftime("%D"), self.start_shift_time,
                time.strftime("%D"), self.end_shift_time)

        return self.object_db.write_to_db(self.sql_connection, self.sql_cursor, sql_query)

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
        try:
            self.performance = round((100 *
                                      self.total_pieces_fabricated() /
                                      ((self.current_work_time - self.current_planned_stop_time - self.current_error_time) / self.cycle_time)), 2)

        except ZeroDivisionError:
            self.performance = 0

        except Exception as e:
            None

        if (self.performance < 0): self.performance = 0
        if (self.performance > 100): self.performance = 100

        return self.performance

    def total_pieces_fabricated(self):
        """
        Select in «table_plc» of the database the total pieces fabricted (OK + NOK)
        where no is breaked or error.
        The night shift has extended for 2 days (22:00 to 06:00), so it must be calculated differently.
        """
        current_time = datetime.now().strftime("%H:%M:%S")

        # Select all pieces fabricated for current shift.
        if (current_time >= '06:00:00' and current_time < '22:00:00'):
            sql_query = "SELECT SUM(OK + NOK) FROM table_plc WHERE (Error = 0 AND Break = 0) AND Date = '{}' AND Hour >= '{}' AND Hour < '{}'".format(
                time.strftime("%D"), self.start_shift_time, self.end_shift_time)

        # If the current time is >= 22:00, the shift is night but the next day hasn't started yet.
        elif (current_time >= "22:00:00"):
            sql_query = "SELECT SUM(OK + NOK) FROM table_plc WHERE (Error = 0 AND Break = 0) AND Date = '{}' AND Hour >= '{}'".format(
                time.strftime("%D"), self.start_shift_time)

        else:
            sql_query = "SELECT SUM(OK + NOK) FROM table_plc WHERE (Error = 0 AND Break = 0) AND ((Date = '{}' AND Hour >= '{}') OR (Date = '{}' AND Hour < '{}'))".format(
                (datetime.today() - timedelta(days = 1)).strftime("%D"), self.start_shift_time,
                time.strftime("%D"), self.end_shift_time)

        return self.object_db.write_to_db(self.sql_connection, self.sql_cursor, sql_query)

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
        try:
            self.quality = round((100 * self.total_pieces_ok_fabricated() / self.total_pieces_fabricated()), 2)

        except ZeroDivisionError:
            self.quality = 0

        if (self.quality < 0): self.quality = 0
        if (self.quality > 100): self.quality = 100

        return self.quality

    def total_pieces_ok_fabricated(self):
        """
        Select from «table_plc» of the database the total pieces fabricated correctly (OK).
        If the current time is < 6AM or > 10PM, the current shift is night.
        It extends for 2 days, so it's calculated differently.
        The night shift has extended for 2 days (22:00 to 06:00), so it must be calculated differently.
        """
        current_time = datetime.now().strftime("%H:%M:%S")

        # Select all pieces fabricated for current shift.
        if (current_time >= '06:00:00' and current_time < '22:00:00'):
            sql_query = "SELECT SUM(OK) FROM table_plc WHERE Error = 0 AND Break = 0 AND Date = '{}' AND Hour >= '{}' AND Hour < '{}'".format(
                time.strftime("%D"), self.start_shift_time, self.end_shift_time)

        # If the current time is >= 22:00, the shift is night but the next day hasn't started yet.
        elif (current_time >= "22:00:00"):
            sql_query = "SELECT SUM(OK) FROM table_plc WHERE Error = 0 AND Break = 0 AND Date = '{}' AND Hour >= '{}'".format(
                time.strftime("%D"), self.start_shift_time)

        else:
            sql_query = "SELECT SUM(OK) FROM table_plc WHERE Error = 0 AND Break = 0 AND ((Date = '{}' AND Hour >= '{}') OR (Date = '{}' AND Hour < '{}'))".format(
                (datetime.today() - timedelta(days = 1)).strftime("%D"), self.start_shift_time,
                time.strftime("%D"), self.end_shift_time)

        return self.object_db.write_to_db(self.sql_connection, self.sql_cursor, sql_query)

if __name__ == '__main__':
    # Start connection.
    sql_path = "/media/rpiiot/CCCOMA_X64F/4246_IOT.db"
    sql_connection = sqlite3.connect(sql_path)
    sql_cursor = sql_connection.cursor()

    # Class OEE.
    current_oee = oee(10, 10, sql_connection, sql_cursor)
    # sql_connection.close()

    """
    print("---------------------------------")
    print("OEE VALUES\n---------------------------------")
    print("\tInterval duration: ", current_oee.interval_duration)
    print("\tCycle time: ", current_oee.cycle_time)
    print("\tNum iterations: ", current_oee.num_iterations)
    print("\tNum maintenances: ", current_oee.num_maintenance)
    print("\tNum errors: ", current_oee.num_error)
    print("\tStart shift hour: ", current_oee.start_shift_time)
    print("\tEnd shift hour: ", current_oee.end_shift_time)
    print("\tBreak shift hour: ", current_oee.break_time)
    """

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
    current_oee.get_break_duration()

    print("---------------------------------")
    print("RESET BEFORE\n---------------------------------")
    print("\tInterval duration: ", current_oee.interval_duration)
    print("\tCycle time: ", current_oee.cycle_time)
    print("\tNum iterations: ", current_oee.num_iterations)
    print("\tNum maintenances: ", current_oee.num_maintenance)
    print("\tNum errors: ", current_oee.num_error)
    print("\tStart shift hour: ", current_oee.start_shift_time)
    print("\tEnd shift hour: ", current_oee.end_shift_time)
    print("\tBreak shift hour: ", current_oee.break_time)

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
    print("\tBreak shift hour: ", current_oee.break_time)

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
    current_oee.get_break_duration()

    print("---------------------------------")
    print("OEE VALUES\n---------------------------------")
    print("\tInterval duration: ", current_oee.interval_duration)
    print("\tCycle time: ", current_oee.cycle_time)
    print("\tNum iterations: ", current_oee.num_iterations)
    print("\tNum maintenances: ", current_oee.num_maintenance)
    print("\tNum errors: ", current_oee.num_error)
    print("\tStart shift hour: ", current_oee.start_shift_time)
    print("\tEnd shift hour: ", current_oee.end_shift_time)
    print("\tBreak shift hour: ", current_oee.break_time)

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
