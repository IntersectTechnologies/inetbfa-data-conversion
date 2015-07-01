# -*- coding: utf-8 -*-
"""
Created on Tue May 19 20:59:02 2015

@author: Niel
"""


import shutil as su
from os import path, listdir, makedirs
import logging

from core.envs import *

slave_paths = [
    path.join('C:\\','root', 'intersect',  'data')
]

def create_dir(directory):
    '''
    '''
    
    if not path.exists(directory):
        makedirs(directory)
        

def sync_latest_master():
    '''
    '''
    
    lu_path = path.join(MASTER_DATA_PATH, 'latest_updates')
    if path.exists(lu_path):
    
        dst = path.join(MASTER_DATA_PATH, 'jse', 'equities', 'daily')
        for f in listdir(lu_path):
            logging.info('Copying file ' + f)
            su.copy(path.join(lu_path, f), dst)
            
        logging.info('Now delete directory' + lu_path)
    
        su.rmtree(lu_path)
    

def sync_master_slave():
    '''
    '''
    
    for fp in slave_paths:
        if path.exists(fp):
            su.rmtree(fp)
        su.copytree(MASTER_DATA_PATH, fp)
    