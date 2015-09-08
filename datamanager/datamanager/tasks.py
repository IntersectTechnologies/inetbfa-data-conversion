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
from quantstrategies.strategies.nwu_momentum import NWUMomentum
from quantstrategies.strategies.growth_portfolio import Momentum

from core.utils import last_month_end, getLog

log = getLog('datamanager')

jse_path = path.join(MASTER_DATA_PATH, 'jse')
fields = MarketData.fields
fields.extend(Dividends.fields)
archive_path = path.join(MASTER_DATA_PATH, str(last_month_end()))

def task_startup():
    if not path.exists(archive_path):
        makedirs(archive_path)


# Portfolio updates


def task_sync_data():
    '''
    '''
    
    sync_latest_master()
    sync_master_slave()