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

fields = MarketData.fields
fields.extend(Dividends.fields)
archive_path = path.join(BACKUP_PATH, str(last_month_end()))

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
    refdata = get_equities()
    prc = MarketDataProcessor()

    dependencies = list(dependencies)
    new_data = prc.load_new(dependencies[0])
    prc.save(new_data, targets[0])

def merge_market_data(dependencies, targets):
    '''
    '''
    
    ref = get_equities()
    prc = MarketDataProcessor()
    dependencies = list(dependencies)
    new = prc.load_old(dependencies[0])
    old = prc.load_old(dependencies[1])
    merged = prc.merge(old, new, ref)
    prc.save(merged, targets[0])

def calc_adjusted_close(dependencies, targets):
    dependencies = list(dependencies)
    adj_close = calc_adj_close(dependencies[0], dependencies[1])
    adj_close.to_csv(targets[0])

##########################################################################################
# DOIT tasks
##########################################################################################

'''
def task_init():
    src = path.join(MASTER_DATA_PATH, "jse", "equities", "daily") 
    for f in listdir(src):
        yield  {
            'name': f,
            'file_dep':[src],
            'actions':['cp %s' % path.join(src, f) + ' %(targets)s'],
            'targets':[path.join(MERGED_PATH, f)]
        }
'''
   
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
            'targets':[path.join(MERGED_PATH, f + '.csv')],
            'file_dep':[path.join(CONVERT_PATH, f + '.csv'), path.join(MASTER_DATA_PATH, "jse", "equities", "daily", f + '.csv')]
        }

def task_calculatedata():
    return {
        'actions':[calc_adjusted_close],
        'file_dep': [path.join(MASTER_DATA_PATH, "jse", "equities", "daily", "Close.csv"),
                     path.join(MASTER_DATA_PATH, "jse", "equities", "daily", "Dividend Ex Date.csv")],
        'targets':[path.join(MASTER_DATA_PATH, "jse", "equities", "daily", "Adjusted Close.csv")]
    }

def task_update():

    return {
        'actions':['cp /c/root/data/merged/* /c/root/data/master/jse/equities/daily/'],
        'file_dep':[MERGED_PATH]
    }

def task_copy():
    gdrivepath = path.join('C:\\','Users','Niel','Google Drive')
    
    return {
        'file_dep':[MASTER_DATA_PATH],
        'actions':['cp -rp %s' % MASTER_DATA_PATH + ' %(targets)s'],
        'targets':[gdrivepath, DATA_PATH]
    }

#TODO:
'''       
def task_archive():
    
    return {
        'actions':[]
        'targets':[path.join(archive_path)]
    }
'''