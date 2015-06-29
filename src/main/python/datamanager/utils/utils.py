# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 14:37:02 2014

@author: Niel
"""
from os import path, listdir, remove
import pandas as pd

# helper functions    
def clear_tempfiles(root):
    '''
    
    '''
    print 'Looking in ' + root + '...'
    if listdir(root):
        # this folder contains files and sub directories
        for f in listdir(root):
            # for every file or sub directory in this directory 
        
            subpath = path.join(root, f)
            if path.isfile(subpath):
                # check if it is a file
                print 'Deleting file: ' + subpath
                # Delete file from directory
                remove(subpath)
            elif path.isdir(subpath):
                # else check if it is a directory
            
                # clear all files in directory and traverse subdirectories
                clear_tempfiles(subpath)
        