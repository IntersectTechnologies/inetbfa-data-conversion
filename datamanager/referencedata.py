# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 15:19:35 2015

@author: Niel
"""

import pandas as pd
import numpy as np
from os import path, listdir
import datetime as dt
from datamanager.datamodel import Equity
from datamanager.envs import *

class ReferenceData(object):
    '''
    TODO: convert referenceprocessor to work the same as the marketdata processeor

    - output a currently listed file -> save output of load_new
    - append historic record of reference data
    '''
    
    def __init__(self):
        '''
        '''
        
        self.fields = ['Industry',
                       'ISIN',
                       'Sector',
                       'Market Data Currency',
                       'Financial Currency',
                       'Ticker',
                       'Listing Status']
         
        self.fieldmap = [('industry', 'Industry', lambda x: (x.strip().split(' - ')[1] if x != 'Unclassified' else 'Unclassified') if (type(x) == unicode or type(x) == str) else 'Unclassified'),
                     ('isin', 'ISIN', lambda x: x.strip() if type(x) == unicode or type(x) == str else x),
                     ('sector', 'Sector', lambda x: (x.strip().split(' - ')[1] if x != 'Unclassified' else 'Unclassified') if (type(x) == unicode or type(x) == str) else 'Unclassified'),
                     ('marketdata_currency', 'Market Data Currency', lambda x: x.strip() if type(x) == unicode or type(x) == str else x),
                     ('financial_currency','Financial Currency', lambda x: x.strip() if (type(x) == unicode or type(x) == str) else x),
                     ('listing_status', 'Listing Status', lambda x: ('CURRENT' if x.strip() == 'Current' else x.strip()) if (type(x) == unicode or type(x) == str) else x),
                     ('fullname', 'Name', lambda x: x.strip() if type(x) == unicode or type(x) == str else x)]

    def convert(self, old, new):
        
        upd = old.copy()
        
        for i in new.index:
            for f1, f2, func in self.fieldmap:  
                new_val = new[f2][i]
                cur_val = upd[f1][i]
                conv_val = func(new_val)
                if i in upd.index:
                    # update
                    if (type(cur_val) == unicode or type(cur_val) == str):
                        if conv_val != cur_val:
                            if conv_val != 'Unclassified': 
                                upd.set_value(i, f1, conv_val)   
                            elif conv_val == 'Unclassified' and cur_val == '':
                                upd.set_value(i, f1, conv_val) 
                else:
                    upd.set_value(i, f1, conv_val)
                    
            upd.set_value(i, 'last_update', str(dt.date.today()))
            
        return upd
