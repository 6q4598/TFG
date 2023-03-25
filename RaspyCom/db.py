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

class db():
    """
    SQL querys.
    """
    def __init__(self):
        self

    def write_to_db(self, connection, cursor, query):
        try:
           cursor.execute(query)
           connection.commit()
           result = cursor.fetchone()[0]
        except:
            print("Error writing to DB: ", query)
            result = -1
        return result if result != None else -1

if __name__=='__main__':
    sql_path = "/media/rpiiot/CCCOMA_X64F/4246_IOT.db"
    sql_connection = sqlite3.connect(sql_path)
    sql_cursor = sql_connection.cursor()
    query = "SELECT COUNT(*) FROM table_plc WHERE Date = '03/21/23' AND Hour >= '14:00:00' AND Hour < '22:00:00';"
    mdb = db()
    result = mdb.write_to_db(sql_connection, sql_cursor, query)
    print(result)
