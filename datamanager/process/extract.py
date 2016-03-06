# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 15:45:10 2014

@author: Niel

THIS CODE IS CURRENTLY NOT USED AND ARE KEPT FOR REFERENCE ALONE
"""

from os import path
import csv
import pandas as pd
from datamanager.envs import MASTER_DATA_PATH

downloads = path.join(data,'downloads','jse','indices', 'csv')
temp = path.join(data, 'temp','indices')
processed = path.join(data, 'processed','indices')

fn = '1994-2004.csv'
rc = 0

with open(path.join(downloads, fn), 'rb') as rfile:
    reader = csv.reader(rfile, delimiter = ',')

    for row in reader:
        if rc == 0:
            header = row
            break
    rc += 1

content = [h for h in header if h!= ''] 
codes = [item.split(' - ')[0] for item in content]
names = [item.split(' - ')[1] for item in content]

df = pd.DataFrame(names, index = codes, columns = ['Name'])
df.to_csv(path.join(processed, 'jse_indices.csv'))

book_value_ps = pd.read_csv(path.join(MASTER_DATA_PATH, 'Book Value Per Share (c).csv'), sep = ',', index_col = 0, parse_dates=True)
price = pd.read_csv(path.join(MASTER_DATA_PATH, 'Price Per Share (c).csv'), sep = ',', index_col = 0, parse_dates=True)
price2book = pd.read_csv(path.join(MASTER_DATA_PATH, 'Price Per Book Value.csv'), sep = ',', index_col = 0, parse_dates=True)

p2b_self = price/book_value_ps
bookvalue_monthly = book_value_ps.resample('M', fill_method='pad')

def read_infochimps(self, _filepath):
    """
    """
    lastcode = ''
    newcode = False

    with open(_filepath,'rb') as srcfile:
        csvreader = csv.reader(srcfile)

        for row in csvreader:
            exchange = row[0]
            code = row[1]

            data = row[1:len(row)-1]

            if csvreader.line_num == 1:
                # currently reading header
                firstline = True;
 
            elif lastcode != code:
                # code has changed from previous row
                newcode = True
                # output current instrument code to console
                print(code)

            if newcode:
                fp = self.create_path(code,exchange)
                # open/create file and write header to file
                destfile = open(fp, 'wb')
                rowWriter = csv.writer(destfile, delimiter=',')
                rowWriter.writerow(header)
                rowWriter.writerow(data)
                newcode = False
            elif firstline:
                header = data
                firstline = False
            else:
                # write data to file
                rowWriter.writerow(data)
        
            lastcode = code

        destfile.close()

def read_sharenet(self, _filepath):
    """
    Read data from Sharenet data service files

    INCOMPLETE:

    - Exception handling
    """
        
    lastcode = ''
    newcode = False

    with open(_filepath,'rb') as srcfile:
        csvreader = csv.reader(srcfile)

        # skip headings
        csvreader.next()
        csvreader.next()
        csvreader.next()
        csvreader.next()
        csvreader.next()

        for row in csvreader:
            try:
                exchange = row[1]
                code = row[2]

                date = row[5][0:4]+'/'+row[5][4:6]+'/'+row[5][6:8]
                
                data = [code,date,row[6],row[7],row[8],row[9],row[10]]

                if lastcode != code:
                    # code has changed from previous row
                    newcode = True
                    # output current instrument code to console
                    print(code)

                if newcode:
                    fp = self.create_path(code,exchange)

                    if os.path.isfile(fp):
                        # file already exists
                        try:
                            destfile = open(fp, 'a');
                            rowWriter = csv.writer(destfile, delimiter=',')
                            rowWriter.writerow(data)
                        except:
                            print('Some error')
                        finally:
                            destfile.close()
                    else:
                        # create file and write header to file
                        try:
                            destfile = open(fp, 'wb');
                            rowWriter = csv.writer(destfile, delimiter=',')
                            rowWriter.writerow(header)
                            rowWriter.writerow(data)
                        except:
                            print('Some error')
                        finally:
                            destfile.close()

                    newcode = False
            except:
                print('Some error')
            finally:    
                lastcode = code