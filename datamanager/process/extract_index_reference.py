# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 15:45:10 2014

@author: Niel
"""

from initialize import data
from os import path
import csv
import pandas as pd

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
