# -*- coding: utf-8 -*-
"""
Created on Fri Dec 05 09:43:45 2014

@author: Niel
"""

import pandas as pd
from os import path

import pyodbc
import pandas.io.sql as psql

from os import path, listdir, makedirs
import sys

import pandas as pd

ref_db = 'Profiledata.mdb'

db_file = path.join('C:\\', 'SMNet', 'Database', 'Profiledata.mdb')
user = ''
password = '44pwc@PM!0107y12*32#'

odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s;UID=%s;PWD=%s' % \
                (db_file, user, password)
                
conn = pyodbc.connect(odbc_conn_str)
cursor = conn.cursor()

# Tables
ref_tables = [
'Address',
'Brands',
'Company',
'ContributionByActivity',
'DirectorDealings',
'Directors',
'Dividends',
'RenamedCompanies',
'SectorClassificationType',
'SecurityCategory',
'ShareBuyBacks',
'Shares',
'SubsAndHoldings',
]

# Reference data

ref = {}

for table in ref_tables:
    sql = ('select * from ' + table)
    cursor = conn.cursor()
    df = psql.frame_query(sql, conn, parse_dates = True)
    ref[table] = df

    
# Import jse equities reference data
data_path = path.join('C:\\', 'root', 'repos', 'data', 'processed', 'jse')

file_p = path.join(data_path, 'jse_equities.csv')
equities = pd.read_csv(file_p, sep = ',', index_col = 0)
ords_ref = pd.read_csv(path.join(data_path, 'ords_reference.csv'), sep=',', index_col = 0)

mc_filep = path.join(data_path, 'market', 'daily', 'Market Cap.csv')
marketcap = pd.read_csv(mc_filep, sep=',', index_col = 0)

def sync_smdb_local(equities, ords_ref):
	'''
	'''
	for ticker in equities.index:
		isin = ords_ref[ords_ref['JSECode']==ticker]['ISIN']
		shortname = ords_ref[ords_ref['JSECode']==ticker]['Shortname']
		status = ords_ref[ords_ref['JSECode']==ticker]['Status']
		if not isin.empty:
			if len(isin) < 2:
				val = isin.iloc[0]
				equities['isin'][ticker] = val
		if not shortname.empty:
			if len(shortname) < 2:
				val = shortname.iloc[0]
				equities['shortname'][ticker] = val	
		if not status.empty:
			if len(status) < 2:
				val = status.iloc[0]
				
				if val == 'D':
					equities['listing_status'][ticker] = 'DELISTED'	
				if val == 'L':
					equities['listing_status'][ticker] = 'LISTED'
					
	return equities

def sync_marketcaps(equities, marketcap):
	'''
	'''
	
	for ticker in equities.index:
		if ticker in marketcap.columns:
			lvi = marketcap[ticker].last_valid_index()
			if lvi:
				mc = marketcap[ticker][lvi]
				equities['market_cap'][ticker] = mc
				equities['last_update'][ticker] = lvi
		else:
			print('No data for ' + ticker)
	
	return equities
	
equities = sync_smdb_local(equities, ords_ref)
equities = sync_marketcaps(equities, marketcap)
equities.to_csv(file_p, index_label = 'ticker')

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