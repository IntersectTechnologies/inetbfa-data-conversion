# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:54:30 2015

@author: Niel
"""

import csv
import sys
import subprocess

def process_file(source, dest):
    '''
    
    '''
    rc = 0
    with open(source, 'rb') as rfile:
        reader = csv.reader(rfile, delimiter = ',')
        with open(dest, 'wb') as wfile:
            writer = csv.writer(wfile, delimiter =',')
            for row in reader:
                if rc == 0:
                    header = row
                    newheader = transform_header(header)
                    writer.writerow(newheader)
                else:
                    writer.writerow(row)
                rc += 1
    
def process_downloads(downloaddir, tempdir):
    '''
    
    '''
    
    merged = merged.swapaxes(0, 2)
    # first clear all temp files in temp directory
    #clear_tempfiles(tempdir)
    
    # process all downloaded market data files and store in temp directory
    for f in listdir(downloaddir): 
        if f.split('.')[1] == 'csv':
            source = path.join(downloaddir, f)
            dest =  path.join(tempdir, f)
            process_file(source, dest)
            
def transform_header(header):
        '''
        
        '''
        newheader = list()
        prev = ''
        for h in header:
            if h!= '':
                prev = h.split(' - ')[0]
            
            newheader.append(prev) 
        
        return newheader    
        
def extract_dividends(source, fns):
        '''
        
        '''
        
        div_dict = {}
        div_items = []
        no_data = []
            
        for fn in fns:
            
            print 'Extracting data from file ' + fn
            xl = pd.ExcelFile(path.join(source, fn))
            
            sheets = xl.sheet_names
            
            rest = [name.split('.')[1] for name in sheets]
            tickers = [name.split('  ')[0].lstrip(' ') for name in rest]
           
            c = 0
    
            for sheet in sheets:
                key = tickers[c]
                if key not in div_dict:
                    try:
                        divs = pd.read_excel(path.join(source, fn), sheetname=sheet, header = 1)
                        # add the dataframes to a dictionary with the ticker as key
                        print 'Adding item: ' + key
                        div_dict[key] = divs
                        div_items.append(key) 
                    except IndexError:
                        if key not in no_data:
                            no_data.append(key) 
                        
                    c += 1
        
        div_panel = pd.Panel(div_dict)
        
        return(div_items, no_data, div_panel)
    
    
    def process_dividend_panel(div_panel, dest, zero):
        '''

        '''
        
        ##############################################################################
        # now create dividend data frames
        
        ea = zero.copy()    # earnings announcements
        ldr = zero.copy()         # last date to register for dividends
        paydate = zero.copy()      # dividend payment date
        amount = zero.copy()      # Dividend Amount
        divtype = zero.copy()      # Dividend Type
        currency = zero.copy()     # Dividend Currency
        
        na_div = []
        # Dates
        for col in zero.columns:
        
            if col in div_panel.items:
                print col
        
                df = div_panel[col]
                
                for date in df['Declaration Date']:
                    # check if date is not NaT
                    if date == date:
                        ea[col].ix[date] = 1
                         
                        # extract dividend type
                        dt = df[df['Declaration Date'] == date]['Dividend Types']
                        curr = df[df['Declaration Date'] == date]['Currency']
                        
                        # Take first of the two dividend types
                        divtype[col].ix[date] = dt.iget(0) 
                        if curr.iget(0) == 'South African Rand':
                            currency[col].ix[date] = 'ZAR'
                        else:
                            print curr.iget(0)
                          
                for date in div_panel[col]['Last Date To Register']:
                    ldr[col].ix[date] = 1
                    
                    # extract dividend amount
                    da = df[df['Last Date To Register'] == date]['Amount']
                    if da.count > 1:
                        # Take the sum of all dividends payed on the same day
                        amount[col].ix[date] = float(da.sum())
                    else:
                        amount[col].ix[date] = float(da)
                    
                for date in div_panel[col]['Payment Date']:
                    paydate[col].ix[date] = 1    
            else:
                na_div.append(col)
            
        ea.to_csv(path.join(dest, 'Earnings Announcement.csv'))
        ldr.to_csv(path.join(dest, 'Last Date To Register.csv'))
        paydate.to_csv(path.join(dest, 'Payment Date.csv'))
        amount.to_csv(path.join(dest, 'Amount.csv'))
        divtype.to_csv(path.join(dest, 'Dividend Type.csv'))
        currency.to_csv(path.join(dest, 'Currency.csv'))
        
    def to_quandl(self):
        '''
        '''
        
        # Initialize paths
        flash = 'H:\\'
        code_path = path.join(flash, 'Werk', 'repos', 'code')
        sys.path.append(code_path)
        
        import preprocessing as prep
        
        data_path = path.join(flash, 'Werk', 'repos', 'data')
        
        downloads = path.join(data_path, 'downloads')
        temp = path.join(data_path, 'temp')
        processed = path.join(data_path, 'processed')
        quandl = path.join(data_path, 'quandl', 'market')
        
        dl_market = path.join(downloads, 'jse', 'market')
        temp_market = path.join(temp, 'jse', 'market')
        proc_market = path.join(processed, 'jse', 'market')
        
        # Load reference data
        equities = pd.read_csv(path.join(processed, 'jse', 'jse_equities.csv'), sep = ',', index_col = 0)
        listed_equities = equities[equities.listing_status == 'LISTED']
        
        startdate = pd.datetime(1990, 1 , 1).date()
        enddate = pd.datetime.today().date()
        
        cal = pd.bdate_range(startdate, enddate)
        
        # trading days - rows
        rows = cal
        
        # all equities - columns

        # create new blank data frame
        dat = np.empty((len(rows), len(cols)))
        dat[:] = np.NAN
        template = pd.DataFrame(dat, index = rows, columns = cols)
        
        # Load data from csv files and save into Panel structures
        prep.process_downloads(dl_market, temp_market)
        
        eqd = {}
        for t in listed_equities.index:
            eqd[t] = template.copy()
            
        pnl = pd.Panel(eqd)
        
        for f in listdir(temp_market):
                
            if f.split('.')[1] == 'csv':
                # read multi index csv file into data frame
                print f
                fn1 = path.join(temp_market, f)
                df = pd.read_csv(fn1, sep = ',', 
                         header = [0,1], index_col = 0, parse_dates = True)
                             
                # extract fields
                for c in df.xs('Close', level = 1, axis = 1).columns:
                    if c in listed_equities.index:
                        print c
                        pnl[c].update(df[c])
                        
        for i in pnl.items:
            print i
            pnl[i].dropna(axis=0, how='all').to_csv(path.join(temp, 'quandl',  'JSE_' + i + '.csv'), index_label = 'Date')
        
        
        skiplist = [
        'ATN',
        'ECSN',
        'TMLP'
        ]
        # Quandl csv flavor
        # YAML header
        
        for f in listdir(path.join(temp, 'quandl')): 
            splits = f.split('.')
            fsuffix = splits[-1]
            if len(splits) > 2:
                ticker = splits[0] + '.' + splits[1]
                print ticker
            else:
                ticker = splits[0]
            if fsuffix == 'csv':
                code = 'code: ' + ticker
                
                realtick = ticker.split('_')[1]
                if realtick not in skiplist:
                    fname = equities['fullname'][realtick]
                    name = 'name: ' + fname
                    priv = 'private: true'
                    desc = 'description: ' + fname + ' daily data'
                    endline = '---'
            
                    header = [[code], [name], [desc], [priv], [endline]]
                    
                    source = path.join(temp, 'quandl', f)
                    dest =  path.join(quandl, f)
                    
                    # Add YAML heading to file
                    with open(source, 'rb') as rfile:
                        reader = csv.reader(rfile, delimiter = ',')
                        with open(dest, 'wb') as wfile:
                            writer = csv.writer(wfile, delimiter =',')
                            writer.writerows(header)        
                            for row in reader:
                                writer.writerow(row)
        
        # Upload data to quandl
        for f in listdir(quandl): 
            fp = path.join(quandl, f)
            
            print 'quandl upload ' + fp
            ret_code = subprocess.call('quandl upload ' + fp, shell = True)