#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import snap7
import sqlite3
import os
from datetime import datetime
from snap7 import util
from threading import *

class algo():

    def __init__(self):
        self.k = 0

    def terra(self):
        self.k += 1

    def reset(self):
        self.k = 0


def test_01(tutu):
    # print(tutu.k, " --- ", end = "")
    tutu.terra()
    if (tutu.k > 5):
        tutu.reset()
    # print(tutu.k, " --- ", end = "\n")

def test_02():
    a = algo()
    l = 0
    while l < 20:
        l += 1
        print(a.k, " --- ", end = "")
        test_01(a)
        print(a.k, " --- ", end = "\n")

def a(b):
    b += 1
    return b

def c(i):
    a(i)
    print(i)

# test_02()
i = 0
c(i)
c(i)
c(i)
