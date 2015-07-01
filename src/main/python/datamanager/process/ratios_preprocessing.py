# -*- coding: utf-8 -*-
"""
Created on Mon Aug 04 12:19:50 2014

@author: Niel

Read ratio data downloaded from expert.mcgregorbfa.com
 and convert to a more convenient format for reading from other applications
 
"""

import pandas as pd
import os

def merge_files(filedir):
    
    counter = 0
    for f in os.listdir(filedir):
        
        # read multi index csv file into data frame
        print 'Adding file: ' + f
        if counter == 0:
            fn1 = filedir + f
            df = pd.read_csv(fn1, sep = ',', 
                     header = [0,1], index_col = 0, parse_dates = True)
        
        else:
            fn2 = filedir + f
            df2 = pd.read_csv(fn2, sep = ',', 
                     header = [0,1], index_col = 0, parse_dates = True)  
    
            df = pd.concat([df, df2], axis = 1)
            
            #df.sort(inplace=True)
        
        counter += 1
            
    return(df)
    
def extract_fields_and_save(df, fields, dest):    
   
   # Close
   for field in fields:
       print 'Extracting ratio ' + field
       sub_df = df.stack().ix[field]
       fn = (field + '.csv').replace('/', 'Per')
       
       print 'Save to ' + fn
       
       sub_df.sort(inplace=True)
       sub_df.to_csv(dest + fn)
        
      
