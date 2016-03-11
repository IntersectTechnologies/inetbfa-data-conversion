# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 14:37:02 2014

@author: Niel
"""
from os import path, listdir, remove
import pandas as pd
import datetime as dt
import calendar as cal
import sys

def last_dayof_prev_month(year, month):
    if (month == 1):
        month = 12
        year = year - 1
        return last_dayof_month(year, month)
    else:
        return last_dayof_month(year, month)

def last_dayof_month(year, month):
    return dt.date(year, month, cal.monthrange(year, month)[1])

def last_month_end():
    td = dt.datetime.today()
    if (td.month == 1):
        lastmonth = 12
        year = td.year - 1
    else:
        lastmonth = td.month - 1
        year = td.year

    enddt = last_dayof_month(year, lastmonth)
    return(enddt)

def date_days_ago(days=0):
    td = dt.datetime.today()
    tmpd = td - dt.timedelta(days=days)

    return str(tmpd.date())

# helper functions    
def clear_tempfiles(root):
    '''
    
    '''
    print('Looking in ' + root + '...')
    if listdir(root):
        # this folder contains files and sub directories
        for f in listdir(root):
            # for every file or sub directory in this directory 
        
            subpath = path.join(root, f)
            if path.isfile(subpath):
                # check if it is a file
                print('Deleting file: ' + subpath)
                # Delete file from directory
                remove(subpath)
            elif path.isdir(subpath):
                # else check if it is a directory
            
                # clear all files in directory and traverse subdirectories
                clear_tempfiles(subpath)
        