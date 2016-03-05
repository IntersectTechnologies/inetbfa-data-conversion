# -*- coding: utf-8 -*-
"""
Created on Tue May 19 20:17:57 2015

@author: Niel
"""
from os import path

dir = path.dirname(__file__)
DATA_ROOT = path.join(dir , '..')
DL_PATH = path.join(DATA_ROOT, 'downloads')
MASTER_DATA_PATH = path.join(DATA_ROOT, 'master')    
CONVERT_PATH = path.join(DATA_ROOT, 'converted')
MERGED_PATH = path.join(DATA_ROOT, 'merged')
