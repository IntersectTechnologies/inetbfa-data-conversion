# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 09:21:57 2014

@author: Niel
"""

from os import path
import pandas as pd
import utils
from initialize import data
import numpy as np

equities = pd.read_csv(path.join(data, 'processed', 'jse_equities.csv'), sep = ',', index_col = 0)

daily_market = path.join(data, 'processed', 'market', 'daily', 'Close.csv')
# create blank template
close = pd.read_csv(daily_market, sep=',', index_col = 0, parse_dates=True)
zero = utils.empty_clone(close)

# trading days - rows
rows = zero.index

# all equities - columns
cols = equities.index

# create new blank data frame
dat = np.empty((len(rows), len(cols)))
dat[:] = np.NAN

template = pd.DataFrame(dat, index = rows, columns = cols)

new_close = template.copy()

# fill template

for c in close.columns:
    print c
    new_close[c] = close[c]
    
# Now add dividends