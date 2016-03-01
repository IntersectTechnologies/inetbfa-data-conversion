# -*- coding: utf-8 -*-
"""
Created on Tue May 19 20:17:57 2015

@author: Niel
"""
from os import path

root = path.join('C:\\', 'root')
DATA_ROOT = path.join(root, 'data')

DL_PATH = path.join(DATA_ROOT, 'downloads')
MASTER_DATA_PATH = path.join(DATA_ROOT, 'master')    

BACKUP_PATH = path.join(root, 'backup')
DATA_PATH = path.join(root, 'workspace', 'data')
CONVERT_PATH = path.join(DATA_ROOT, 'converted')
MERGED_PATH = path.join(DATA_ROOT, 'merged')
PORTFOLIO_PATH = path.join(DATA_ROOT, 'portfolios')
MODEL_PATH = path.join(DATA_ROOT, 'models')
INDICES_PATH = path.join(DATA_ROOT, 'indices')
TRANSACT_PATH = path.join(DATA_ROOT, 'transactions')

'''
Directory structure:
    root/{exchange}/{security-type}/{frequency}
    
'''