from os import path, listdir, makedirs
import re, codecs
import datetime as dt
import calendar as cal

from datamanager.envs import *
from datamanager.datamodel import MarketData, Dividends
from datamanager.load import get_equities, set_equities # update_listing_status
from datamanager.process_downloads import MarketDataProcessor, ReferenceProcessor
from datamanager.sync import create_dir, sync_latest_master, sync_master_slave
from datamanager.adjust import calc_adj_close

from core.utils import last_month_end

#log = getLog('datamanager')

jse_path = path.join(MASTER_DATA_PATH, 'jse')
fields = MarketData.fields
fields.extend(Dividends.fields)
archive_path = path.join(MASTER_DATA_PATH, str(last_month_end()))

def convert_ref_data(dependencies, targets):
    '''
    '''

    dependencies = list(dependencies)
    #log.info('Converting reference data')
    ref = get_equities()
    refp = ReferenceProcessor()

    refnew = refp.load_new(dependencies[0])
    # Update path to write to
    refnew.to_csv(targets[0])

def convert_market_data(dependencies, targets):
    ref = get_equities()
    prc = MarketDataProcessor()

    dependencies = list(dependencies)
    new_data = prc.load_new(dependencies[0])
    prc.save(new_data, targets[0])

def merge_market_data(dependencies, targets):
    '''
    '''
    
    ref = get_equities()
    prc = MarketDataProcessor()

    #merged = prc.load_and_merge(f, MarketData.filepath, DL_PATH, ref)
    #prc.save(merged, targets[0])

def calc_adjusted_close(dependencies, targets):
    dependencies = list(dependencies)
    adj_close = calc_adj_close(dependencies[0], dependencies[1])
    adj_close.to_csv(targets[0])

def task_convertrefdata():
    return {
        'actions': [convert_ref_data],
        'file_dep': [path.join(DL_PATH, 'Reference.xlsx')],
        'targets':[path.join(CONVERT_PATH, 'jse_equities.csv')]
    }


def task_convertmarketdata():
    for f in fields:
        yield {
            'name':f,
            'actions':[convert_market_data],
            'targets':[path.join(CONVERT_PATH, f+ '.csv')],
            'file_dep':[path.join(DL_PATH, f + '.xlsx')]
        }

def task_mergemarketdata():
    for f in fields:
        yield {
            'name':f,
            'actions':[merge_market_data],
            'targets':[path.join(MASTER_DATA_PATH, 'jse', 'equities', 'daily', f+ '.csv')],
            'file_dep':[path.join(CONVERT_PATH, f + '.csv')]
        }

def task_calculate():
    return {
        'actions':[calc_adjusted_close],
        'file_dep': [path.join(MASTER_DATA_PATH, "jse", "equities", "daily", "Close.csv"),
                     path.join(MASTER_DATA_PATH, "jse", "equities", "daily", "Dividend Ex Date.csv")],
        'targets':[path.join(MASTER_DATA_PATH, "jse", "equities", "daily",'Adjusted Close.csv')]
    }

def task_copy():
    return {
        'file_dep':[],
        'actions':['cp %(dependencies)s %(targets)s'],
        'targets':[]
    }

def task_archive():
    return {
        'actions':[]
    }