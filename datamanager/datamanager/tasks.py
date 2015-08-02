from os import path, listdir
import re, codecs
import logging
import datetime as dt
import calendar as cal

from datamanager.envs import *
from datamanager.datamodel import MarketData, Dividends
from datamanager.load import get_equities, set_equities # update_listing_status
from datamanager.process_downloads import MarketDataProcessor, ReferenceProcessor
from datamanager.sync import create_dir, sync_latest_master, sync_master_slave
from datamanager.adjust import calc_adj_close
from quantstrategies.strategies.nwu_momentum import NWUMomentum

from core.utils import last_month_end

# logging
logging.basicConfig(filename='datamanager.log', level=logging.INFO)

jse_path = path.join(MASTER_DATA_PATH, 'jse')
fields = MarketData.fields
fields.extend(Dividends.fields)

archive_path = path.join(MASTER_DATA_PATH, last_month_end())
def task_startup():

    if not os.path.exists(archive_path):
        os.makedirs(archive_path)

def task_calc_adjusted_close():
    adj_close = calc_adj_close()
    adj_close.to_csv(path.join(MASTER_DATA_PATH, 'jse' , 'equities', 'daily', 'Adjusted Close.csv'))

def task_update_nwu_momentum_portfolio():
    
    enddt = last_month_end()
    tmpd = enddt - dt.timedelta(days=365)
    startdt = dt.date(tmpd.year, tmpd.month+1, 1)
    mom = NWUMomentum(startdt, enddt)

    mom.calc_momentum()
    mom.save()

def task_update_ref_data():
    '''
    '''
    ref = get_equities()
    refp = ReferenceProcessor()
    refnew = refp.load_new(DL_PATH)
    
    # Update path to write to
    refnew.to_csv(path.join(archive_path, 'jse_equities.csv'))

def task_update_market_data():
    '''
    '''
    
    avail_fields = [f.split('.')[0] for f in listdir(DL_PATH)]
    ref = get_equities()
    prc = MarketDataProcessor(ref)
    create_dir(path.join(MASTER_DATA_PATH, 'latest_updates'))
    
    logging.info('Start processing updated data files...')
    for f in avail_fields:
        if f in fields and f != 'Reference':
            logging.info('Processing ' + f)
            merged = prc.load_and_merge(f, MarketData.filepath, DL_PATH)
            logging.info('Saving data to: '+ path.join(MASTER_DATA_PATH, 'latest_updates', f + '.csv'))
            prc.save(merged, path.join(MASTER_DATA_PATH, 'latest_updates', f + '.csv'))
            logging.info('Finished processing file...')
    
    logging.info('Finished processing Market and Dividend Data')

def task_sync_data():
    '''
    '''
    
    sync_latest_master()
    sync_master_slave()