from os import path, listdir, makedirs
import re, codecs
import datetime as dt
import calendar as cal
import pandas as pd
import string
import numpy as np

from datamanager.envs import *
from datamanager.load import *
from datamanager.adjust import calc_adj_close, calc_booktomarket
from datamanager.utils import last_month_end
import datamanager.transforms as transf
fields = marketdata_fields()

# paths
mergein_old = MASTER_DATA_PATH
mergein_new = CONVERT_PATH

index_src_path = path.join(DL_PATH, 'Indices.xlsx')
closepath = path.join(MERGED_PATH, "Close.csv")
divpath = path.join(MERGED_PATH, "Dividend Ex Date.csv")
bookvaluepath = path.join(MERGED_PATH, "Book Value per Share.csv")

def get_all_equities():
    new_all, _, _, _ = get_all_equities_from_data(MERGED_PATH, CONVERT_PATH, 'Close')
    return new_all

def get_current_listed():
    new_all, current, newly_listed, delisted = get_all_equities_from_data(MERGED_PATH, CONVERT_PATH, 'Close')
    return current_set

def convert_data(task):
    '''
    '''
    name = task.name.split(':')[1]
    fp = path.join(DL_PATH, name + '.xlsx')
    new_data = load_intebfa_ts_data(fp)

    # drop all data for current month
    
    dropix = new_data.index[new_data.index.values.astype('datetime64[D]') > np.datetime64(last_month_end())]
    new_data.drop(dropix).to_csv(task.targets[0])

def convert_indices(task):
    new_data = load_inetbfa_ts_data(index_src_path)
    dropix = new_data.index[new_data.index.values.astype('datetime64[D]') > np.datetime64(last_month_end())]
    new_data.drop(dropix).to_csv(task.targets[0])

def merge_data(task): 
    
    name = task.name.split(':')[1]
    new = load_ts(path.join(CONVERT_PATH, name + '.csv'))
    old = load_ts(path.join(MASTER_DATA_PATH, name + '.csv'))
    
    merged = empty_dataframe(get_all_equities())
    merged.update(old)
    merged.update(new)
          
    merged.to_csv(task.targets[0])

def calc_adjusted_close(dependencies, targets):
    all_equities = get_all_equities()

    # Import closing price data
    close = load_field_ts(MERGED_PATH, field = "Close")

    # Import dividend ex date data
    divs = load_field_ts(MERGED_PATH, field = "Dividend Ex Date")
    adj_close = calc_adj_close(close, divs, all_equities)
    adj_close.to_csv(targets[0])

def booktomarket(dependencies, targets):
    # Import closing price data
    close = load_field_ts(MERGED_PATH, field = "Close")

    # Import book value per share data
    bookvalue = load_field_ts(MERGED_PATH, field = "Book Value per Share")
    b2m = calc_booktomarket(close, bookvalue)
    b2m.to_csv(targets[0])

def resample_monthly(task):

    name = task.name.split(':')[1]
    data = load_field_ts(MASTER_DATA_PATH, field = name)
    
    write = True
    out = pd.DataFrame()

    if name == 'Close':
        out = transf.resample_monthly(data, how = 'last')
    elif name == 'Adjusted Close':
        out = transf.resample_monthly(data, how = 'last')
    elif name == 'Open':
        out = transf.resample_monthly(data, how = 'first')
    elif name == 'High':
        out = transf.resample_monthly(data, how = 'max')
    elif name == 'Low':
        out = transf.resample_monthly(data, how = 'min')
    elif name == 'DY':
        out = transf.resample_monthly(data, how = 'last')
    elif name == 'EY':
        out = transf.resample_monthly(data, how = 'last')
    elif name == 'PE':
        out = transf.resample_monthly(data, how = 'last')
    elif name == 'Book-to-Market':
        out = transf.resample_monthly(data, how = 'last')
    elif name == 'Volume':
        out = transf.resample_monthly(data, how = 'sum')
    elif name == 'Total Number Of Shares':
        out = transf.resample_monthly(data, how = 'last')
    elif name == 'Number Of Trades':
        out = transf.resample_monthly(data, how = 'sum')
    elif name == 'Market Cap':
        out = transf.resample_monthly(data, how = 'last')
    else:
        write = False
    
    if (write):
        out.to_csv(path.join(MASTER_DATA_PATH, name + '-monthly.csv'))

def monthly_avg_momentum(task):
    # load the daily close
    close = load_field_ts(MASTER_DATA_PATH, field = "Close")

    # resample to monthly average data
    close_m = transf.resample_monthly(close, how = 'mean')
    
    # calculate the momentum
    mom = transf.momentum_monthly(close_m, 12, 1)
    mom.to_csv(path.join(MASTER_DATA_PATH, "Monthly-Avg-Momentum.csv"))

def monthly_close_momentum(task):
    # load the daily close
    close = load_field_ts(MASTER_DATA_PATH, field = "Close")

    # resample to monthly close data
    close_m = transf.resample_monthly(close, how = 'last')
    
    # calculate the momentum
    mom = transf.momentum_monthly(close_m, 12, 1)
    mom.to_csv(path.join(MASTER_DATA_PATH, "Monthly-Close-Momentum.csv"))

def calc_log_returns(task):
    close = load_field_ts(MASTER_DATA_PATH, field = "Close")

    logret = transf.log_returns(close)
    logret.to_csv(path.join(MASTER_DATA_PATH, "Log-Returns.csv"))

def calc_pead_momentum(task):
    # load close
    close = load_field_ts(MASTER_DATA_PATH, field = "Close")

    # load dividend decl date
    announcements = load_field_ts(MASTER_DATA_PATH, field = "Dividend Declaration Date")
    pead = transf.pead_momentum(announcements, close)

    pead.to_csv(path.join(MASTER_DATA_PATH, "Normalized-PEAD-Momentum.csv"))

def swapaxes(dependencies, targets):
    
    temp = {}
    for d in dependencies:
        field = d.split("\\")[-1].split(".")[0]
        temp[field] = pd.read_csv(d, sep = ',', index_col = 0, parse_dates=True)

    # now create panel
    panel = pd.Panel(temp)
    out = panel.swapaxes(0, 2)

    for ticker in out.items:
        out[ticker].dropna(how='all').to_csv(path.join(CONVERT_PATH, "tickers", ticker + '.csv'), index_label = "Date")

##########################################################################################
# DOIT tasks
##########################################################################################

# 1
def task_convert():
    for f in fields:
        yield {
            'name':f,
            'actions':[convert_data],
            'targets':[path.join(CONVERT_PATH, f+ '.csv')],
            'file_dep':[path.join(DL_PATH, f + '.xlsx')],
        }

def task_convert_index():
     return {
        'actions':[convert_indices],
        'file_dep': [path.join(DL_PATH, 'Indices.xlsx')],
        'targets':[path.join(MERGED_PATH, "Indices.csv")]
    }

# 2
def task_merge():
    for f in fields:
        yield {
            'name':f,
            'actions':[merge_data],
            'targets':[path.join(MERGED_PATH, f + '.csv')],
            'file_dep':[path.join(mergein_new, f + '.csv'), path.join(mergein_old, f + '.csv')]
        }
# 3
def task_adjusted_close():
    return {
        'actions':[calc_adjusted_close],
        'file_dep': [closepath,
                     divpath],
        'targets':[path.join(MERGED_PATH, "Adjusted Close.csv")]
    }

# 5
def task_book2market():
    return {
        'actions':[booktomarket],
        'file_dep': [closepath, bookvaluepath],
        'targets':[path.join(MERGED_PATH, "Book-to-Market.csv")]
    }

# 6
def task_data_per_ticker():
    files = [path.join(CONVERT_PATH, f + '.csv') for f in fields]
    return {
        'actions':[swapaxes],
        'file_dep': files,
        'targets':[path.join(CONVERT_PATH, "tickers")]
    }

def task_resample_monthly():
    expanded = fields + ['Book-to-Market', 'Adjusted Close']
    for f in fields:
        yield {
            'name':f,
            'actions':[resample_monthly],
            'targets':[path.join(MASTER_DATA_PATH, f + '-monthly.csv')],
            'file_dep':[path.join(MASTER_DATA_PATH, f + '.csv')],
        }

def task_monthly_close_momentum():
    return {
        'actions':[monthly_close_momentum],
        'file_dep':[path.join(MASTER_DATA_PATH, 'Close.csv')],
    }

def task_monthly_avg_momentum():
    return {
        'actions':[monthly_avg_momentum],
        'file_dep':[path.join(MASTER_DATA_PATH, 'Close.csv')],
        'targets':[path.join(MASTER_DATA_PATH, "Monthly-Avg-Momentum.csv")]
    }

def task_log_returns():
    return {
        'actions':[calc_log_returns],
        'file_dep':[path.join(MASTER_DATA_PATH, 'Close.csv')],
    }

def task_pead_momentum():
    return {
        'actions':[calc_pead_momentum],
        'file_dep':[path.join(MASTER_DATA_PATH, 'Close.csv'), path.join(MASTER_DATA_PATH, 'Dividend Declaration Date.csv')],
        'targets':[path.join(MASTER_DATA_PATH, "Normalized-PEAD-Momentum.csv")]
    }