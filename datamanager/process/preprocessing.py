'''
THIS CODE IS CURRENTLY NOT USED AND ARE KEPT FOR REFERENCE ALONE
'''

import pandas as pd
from os import listdir, path
import csv    


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

def merge_files(filedir):
    
    counter = 0
    for f in os.listdir(filedir):
        
        # read multi index csv file into data frame
        print('Adding file: ' + f)
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
       print('Extracting ratio ' + field)
       sub_df = df.stack().ix[field]
       fn = (field + '.csv').replace('/', 'Per')
       
       print('Save to ' + fn)
       
       sub_df.sort(inplace=True)
       sub_df.to_csv(dest + fn)
        
def merge_files(filedir):
    
    counter = 0
    for f in listdir(filedir):
        
        # read multi index csv file into data frame
        print('Adding file: ' + f)
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
       print('Extracting ratio ' + field)
       sub_df = df.stack().ix[field]
       fn = (field + '.csv').replace('/', 'Per')
       
       print('Save to ' + fn)
       
       sub_df.sort(inplace=True)
       sub_df.to_csv(dest + fn)

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
       
def extract_data(filedir, panel, fields):
    '''
    This function looks in the directory filedir for all csv data files and reads them into memory
    The fields provided by the fields parameter are extracted for each file
    and saved in the panel datastructure
    
    The panel datastructure are returned when finished with all files
    
    If the data overlaps, the last file's data will be used
    '''

    for f in listdir(filedir):
        
        if f.split('.')[1] == 'csv':
            # read multi index csv file into data frame
            print(f)
            fn1 = path.join(filedir, f)
            df = pd.read_csv(fn1, sep = ',', 
                     header = [0,1], index_col = 0, parse_dates = True)
                         
            # extract fields
            for field in fields:
                print('Extracting ' + field)
                sub = df.xs(field, level = 1, axis = 1)
                panel[field].update(sub)
                
    return(panel)    

def resample_monthly(source, dest, field):
    '''
    
    '''
    price = pd.read_csv(path.join(source, field + '.csv'), sep = ',', index_col = 0, parse_dates = True)
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
    elif field == 'DY':
        price_monthly = price.resample('M', how = 'last')
    elif field == 'EY':
        price_monthly = price.resample('M', how = 'last')
    elif field == 'PE':
        price_monthly = price.resample('M', how = 'last')
    elif field == 'VWAP':
        raise Exception('VWAP is calculated separately...')
    else:
        raise Exception('"' + field + '" currently not supported')
    
    # Now write to destination folder
    price_monthly.to_csv(path.join(dest, field + '.csv'))    
    
def calc_monthly_vwap(price, vol):
    '''
    Calculate monthly VWAP from price and volume data
    '''
    
    value = price*vol
    vol_m = vol.resample('M', how = 'sum')
    vwap = value.resample('M', how = 'sum')/vol_m

    return(vwap)
    

downloads = path.join(data,'downloads','jse','ratios')
temp = path.join(data, 'temp','ratios')
processed = path.join(data, 'processed','ratios')

# source folders
listed_ratios = path.join(downloads, 'listed','csv')
delisted_ratios = path.join(downloads, 'delisted','csv')

prep.process_downloads(listed_ratios, path.join(temp , 'listed'))
#process_downloads(delisted_ratios, temp + 'delisted/')

merged = rp.merge_files(path.join(temp, 'listed'))

rp.extract_fields_and_save(merged, ratios, processed)

# Resample Ratios


# Process index data

downloads = path.join(data,'downloads','jse','indices', 'csv')
temp = path.join(data, 'temp','indices')
processed = path.join(data, 'processed','indices')            

prep.process_downloads(downloads, temp)
merged = ip.merge_files(temp)

ip.extract_fields_and_save(merged, index_fields, processed)

# Dividend Preprocessing


source = path.join(data, 'downloads', 'jse', 'dividends')
fns = listdir(source)
div_items, no_data, div_panel = dp.extract_dividends(source, fns)

daily_market = path.join(data, 'processed', 'market', 'daily', 'Close.csv')
close = pd.read_csv(daily_market, sep=',', index_col = 0, parse_dates=True)

zero = empty_clone(close)

dp.process_dividend_panel(div_panel,  path.join(data, 'processed', 'dividends', 'daily'), zero)