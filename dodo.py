from os import path, listdir, makedirs
import re, codecs
import datetime as dt
import calendar as cal
import pandas as pd
import string

from datamanager.envs import *
from datamanager.load import *
from datamanager.adjust import calc_adj_close, calc_booktomarket
from datamanager.utils import last_month_end

fields = marketdata_fields()

# paths
mergein_old = MASTER_DATA_PATH
mergein_new = CONVERT_PATH

closepath = path.join(MERGED_PATH, "Close.csv")
divpath = path.join(MERGED_PATH, "Dividend Ex Date.csv")
bookvaluepath = path.join(MERGED_PATH, "Book Value per Share.csv")

def get_all_equities():
    new_all, _, _, _ = get_all_equities_from_data(MERGED_PATH, CONVERT_PATH, 'Close')
    return new_all

def get_current_listed():
    new_all, current, newly_listed, delisted = get_all_equities_from_data(MERGED_PATH, CONVERT_PATH, 'Close')
    return current_set

def convert_ref_data(dependencies, targets):
    '''
    '''

    dependencies = list(dependencies)

    refnew = load_inetbfa_ref_data(dependencies[0])
    # Update path to write to
    refnew.to_csv(targets[0])
    listed_equities = list(refnew.index)

def convert_market_data(dependencies, targets):
    '''
    '''
    dependencies = list(dependencies)
    new_data = load_intebfa_ts_data(dependencies[0])
    new_data = new_data.dropna(how='all')
    new_data.to_csv(targets[0])

def calculate_conversion_report():
    '''
    '''

def merge_ref_data(dependencies, targets):
    old = get_all_equities()
    
def merge_market_data(task): 
  
    new = load_ts(path.join(CONVERT_PATH, task.name.split(':')[1] + '.csv'))
    old = load_ts(path.join(MASTER_DATA_PATH, task.name.split(':')[1] + '.csv'))
    
    merged = empty_dataframe(get_all_equities())
    merged.update(old)
    merged.update(new)

    merged = merged.dropna(how='all')
    merged.to_csv(targets[0])

def calc_adjusted_close(dependencies, targets):
    all_equities = get_all_equities()
    adj_close = calc_adj_close(closepath, divpath, all_equities)
    adj_close.to_csv(targets[0])

def booktomarket(dependencies, targets):
    b2m = calc_booktomarket(closepath, bookvaluepath)
    b2m.to_csv(targets[0])

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
def task_convertrefdata():
    return {
        'actions': [convert_ref_data],
        'file_dep': [path.join(DL_PATH, 'Reference.xlsx')],
        'targets':[path.join(CONVERT_PATH, 'jse_equities.csv')]
    }

# 2
def task_convertmarketdata():
    for f in fields:
        yield {
            'name':f,
            'actions':[convert_market_data],
            'targets':[path.join(CONVERT_PATH, f+ '.csv')],
            'file_dep':[path.join(DL_PATH, f + '.xlsx')],
            'task_dep':['convertrefdata']
        }

# 3
def task_mergemarketdata():
    for f in fields:
        yield {
            'name':f,
            'actions':[merge_market_data],
            'targets':[path.join(MERGED_PATH, f + '.csv')],
            'file_dep':[path.join(mergein_new, f + '.csv'), path.join(mergein_old, f + '.csv'), path.join(MERGED_PATH, 'jse_equities.csv')]
        }
# 4
def task_calculatedata():
    return {
        'actions':[calc_adjusted_close],
        'file_dep': [closepath,
                     divpath],
        'targets':[path.join(MERGED_PATH, "Adjusted Close.csv")]
    }

# 5
def task_booktomarket():
    return {
        'actions':[booktomarket],
        'file_dep': [closepath,
                     bookvaluepath],
        'targets':[path.join(MERGED_PATH, "Book-to-Market.csv")]
    }

# 6
def task_swap():
    files = [path.join(CONVERT_PATH, f + '.csv') for f in fields]
    return {
        'actions':[swapaxes],
        'file_dep': files,
        'targets':[path.join(CONVERT_PATH, "tickers")]
    }