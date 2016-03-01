# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 14:22:44 2014

@author: Niel
"""

import pandas as pd
from os import path, listdir

def merge_files(filedir):
    '''
    
    '''
    counter = 0
    for f in listdir(filedir):
        
        # read multi index csv file into data frame
        print('Adding file: ' + f)
        if counter == 0:
            fn1 = path.join(filedir, f)
            df = pd.read_csv(fn1, sep = ',', 
                     header = [0,1], index_col = 0, parse_dates = True)
        
        else:
            fn2 = path.join(filedir, f)
            df2 = pd.read_csv(fn2, sep = ',', 
                     header = [0,1], index_col = 0, parse_dates = True)  
    
            df = pd.concat([df, df2])
        counter += 1
            
    return(df)

def extract_fields_and_save(df, fields, dest):    
   '''
   
   '''
   
   for field in fields:
       print('Extracting ' + field)
       sub_df = df.xs(field, level = 1, axis = 1)
       fn = field + '.csv'
       
       sub_df.sort(inplace=True)
       
       sub_df.drop(sub_df[sub_df.isnull().all(axis=1)].index, inplace=True)
       sub_df.to_csv(path.join(dest, fn))
    

def resample_monthly(source, dest, field):
    '''
    
    '''
    price = pd.read_csv(source, sep = ',', index_col = 0, parse_dates = True)
    price.sort(inplace = True)

    if field == 'Close':
        price_monthly = price.resample('M', how = 'last')
    elif field == 'Open':
        price_monthly = price.resample('M', how = 'first')
    elif field == 'High':
        price_monthly = price.resample('M', how = 'max')
    elif field == 'Low':
        price_monthly = price.resample('M', how = 'min')
    elif field == 'Volume':
        price_monthly = price.resample('M', how = 'sum')
    elif field == 'Total Number Of Shares':
        price_monthly = price.resample('M', how = 'last')
    elif field == 'Number Of Trades':
        price_monthly = price.resample('M', how = 'sum')
    elif field == 'Market Cap':
        price_monthly = price.resample('M', how = 'last')
    elif field == 'VWAP':
        print('VWAP is calculated separately...')
    else:
        raise Exception('"' + field + '" currently not supported')
    
    # Now write to destination folder
    price_monthly.to_csv(path.join(dest, field + '.csv'))