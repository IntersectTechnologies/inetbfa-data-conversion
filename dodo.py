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

def convert_ref_data():
    '''
    '''
    #log.info('Converting reference data')
    ref = get_equities()
    refp = ReferenceProcessor()
    refnew = refp.load_new(DL_PATH)
    
    # Update path to write to
    refnew.to_csv(path.join(archive_path, 'jse_equities.csv'))

def convert_market_data():
    avail_fields = [f.split('.')[0] for f in listdir(DL_PATH)]
    ref = get_equities()
    prc = MarketDataProcessor()

    #create_dir(path.join(MASTER_DATA_PATH, 'latest_updates'))
    #log.info('Start converting downloaded data files...')
    for f in avail_fields:
        if f in fields and f != 'Reference':
            #log.info('Processing ' + f)
            new_data = prc.load_new(f, DL_PATH)
            #log.info('Saving data to: '+ path.join(archive_path, f + '.csv'))
            prc.save(new_data, path.join(archive_path, f + '.csv'))

def merge_ref_data():
    '''
    '''
    ref = get_equities()
    refp = ReferenceProcessor()
    refnew = refp.load_new(DL_PATH)
    
    #log.info('Merging reference data')

    # Update path to write to
    refnew.to_csv(path.join(MASTER_DATA_PATH, 'jse_equities.csv'))

def merge_market_data():
    '''
    '''
    
    avail_fields = [f.split('.')[0] for f in listdir(DL_PATH)]
    ref = get_equities()
    prc = MarketDataProcessor()
    
    for f in avail_fields:
        if f in fields and f != 'Reference':
            merged = prc.load_and_merge(f, MarketData.filepath, DL_PATH, ref)
            prc.save(merged, path.join(MASTER_DATA_PATH, 'jse', 'equities', 'daily', f + '.csv'))

def calc_adjusted_close():
    adj_close = calc_adj_close()
    adj_close.to_csv(path.join(MASTER_DATA_PATH, 'jse' , 'equities', 'daily', 'Adjusted Close.csv'))

def task_convert():
    return {
        'actions': [convert_ref_data, convert_market_data],
        'file_dep': [],
        'targets':[]
    }

def task_merge():
    return {
        'actions':[merge_ref_data, merge_market_data],
        'targets':[path.join(MASTER_DATA_PATH, 'jse', 'equities', 'daily')]
    }

def task_calculate():
    return {
        'actions':[calc_adjusted_close],
        'targets':[]
    }
