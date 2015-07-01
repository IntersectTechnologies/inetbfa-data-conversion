# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 15:50:32 2014

@author: Niel

Analysis playground
"""

import pandas as pd

from os import path
from initialize import data
from pylab import *

source = path.join(data, 'processed', 'indices')

# load index Close data
index_close = pd.read_csv(path.join(source, 'Close.csv'), index_col = 0, parse_dates = True)

index_close.J200.plot()

simple_ret = index_close.pct_change()
simple_ret.J200.plot()

cum_ret = simple_ret.cumsum()
cum_ret.J200.plot()

# calculate rolling wiwnow stats for JSE Top 40 Index

# Rolling 12 month returns

trading_days = 252
ret_roll_12m = pd.rolling_sum(simple_ret, window = trading_days, min_periods = 10)
ret_roll_12m.J200.plot()

ret_roll_24m = pd.rolling_sum(simple_ret, window = trading_days * 2, min_periods = 10)
ret_roll_24m.J200.plot()

ret_roll_36m = pd.rolling_sum(simple_ret, window = trading_days * 3, min_periods = 10)
ret_roll_36m.J200.plot()

ret_roll_36m.mean().plot(kind='bar')

# histogram plot
mean_roll_36m = ret_roll_36m.mean()
mean_roll_36m[mean_roll_36m < mean_roll_36m.std()].hist(bins=15)

log_ret = log(index_close) - log(index_close.shift(1))

# Monthly index datas
index_close_monthly = index_close.resample('M', how='last')
log_ret_monthly = log(index_close_monthly) - log(index_close_monthly.shift(1))

roll_12m_ret = pd.rolling_sum(log_ret_monthly, 12, min_periods = 3)

# Correlation between the past 3 month's return and the coming 3 month's return
j200 = pd.DataFrame({'J200_Past': roll_12m_ret.J200, 'J200_Future': roll_12m_ret.shift(-12).J200})
correl_12m = j200[j200>j200.std()].corr()

j200_norm = j200 - j200.mean()

# Positive extreme - likelihood of extreme positive year followed by another good year
xtrm_correl_pos = j200_norm[j200_norm.J200_Past > 0.25*j200.std()['J200_Past']].corr()
print 'Correlation between positive past 12 month return with future 12 month return'
print xtrm_correl_pos
print 'Number of Observations: '
print j200_norm[j200_norm.J200_Past > 0.25*j200.std()['J200_Past']].count()

print 'Average Return in past and Future 12 months (Positive): '
print j200[j200_norm.J200_Past > 0.25*j200.std()['J200_Past']].mean()

# Negative extreme
xtrm_correl_neg = j200_norm[j200_norm.J200_Past < -0.25*j200.std()['J200_Past']].corr()
print 'Correlation between negative past 12 month return with future 12 month return'
print xtrm_correl_neg
print 'Number of Observations: '  
print j200_norm[j200_norm.J200_Past < -0.25*j200.std()['J200_Past']].count()

print 'Average Return in past and Future 12 months (Negative): '
print j200[j200_norm.J200_Past < -0.25*j200.std()['J200_Past']].mean()

print 'Overall average return in any 12 month period: '
print j200.mean()