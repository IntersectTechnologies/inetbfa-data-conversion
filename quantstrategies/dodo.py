
from os import path, listdir, makedirs
import re, codecs
import datetime as dt
import calendar as cal

from datamanager.envs import *
from datamanager.load import get_equities, set_equities # update_listing_status
from datamanager.process_downloads import MarketDataProcessor, ReferenceProcessor
from datamanager.sync import create_dir, sync_latest_master, sync_master_slave
from datamanager.adjust import calc_adj_close

from core.utils import last_month_end

def update_nwu_momentum_portfolio():
    
    enddt = last_month_end()
    tmpd = enddt - dt.timedelta(days=365)
    startdt = dt.date(tmpd.year, tmpd.month+1, 1)
    mom = NWUMomentum(startdt, enddt)

    mom.calc_momentum()
    mom.save()

def update_growth_portfolio():
    enddt = last_month_end()
    tmpd = enddt - dt.timedelta(days=365)
    startdt = dt.date(tmpd.year, tmpd.month+1, 1)
    mom = Momentum(startdt, enddt)

    mom.calc_momentum()
    mom.save()


def task_portfolio_momentum():
    return {
        'actions':['update_nwu_momentum_portfolio']
        'targets':[]
    }
    
 def task_portfolio_growth():
    return {
        'actions':['update_growth_portfolio']
        'targets':[]
    }