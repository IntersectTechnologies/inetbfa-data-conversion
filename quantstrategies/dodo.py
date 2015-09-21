from os import path, listdir, makedirs
import re, codecs
import datetime as dt
import calendar as cal

from datamanager.envs import *
from quantstrategies.strategies.nwu_momentum import NWUMomentum
from quantstrategies.strategies.growth_portfolio import GrowthPortfolio
from quantstrategies.strategies.detrended_oscillator import DetrendedOscillator
from core.utils import last_month_end

enddt = last_month_end()
tmpd = enddt - dt.timedelta(days=365)
startdt = dt.date(tmpd.year, tmpd.month+1, 1)

def update_nwu_momentum_portfolio(dependencies, targets):
    mom = NWUMomentum(startdt, enddt)
    mom.save(targets[0])

def update_growth_portfolio(dependencies, targets):
    mom = GrowthPortfolio(startdt, enddt)
    mom.save(targets[0])

def update_detrended_oscillator_portfolio(dependencies, targets):
    do = DetrendedOscillator(startdt, enddt)
    do.save(targets[0])  
    
   
def task_portfolio_momentum():
    return {
        'actions':[update_nwu_momentum_portfolio],
        'targets':[path.join(MODEL_PATH, 'NWU Momentum Portfolio-' + str(last_month_end()) + '.xlsx' )]
    }
    
def task_portfolio_growth():
    return {
        'actions':[update_growth_portfolio],
        'targets':[path.join(MODEL_PATH, 'Growth Portfolio-' + str(last_month_end()) + '.xlsx' )]
    }

def task_portfolio_detrended_oscillator():
    return {
        'actions':[update_detrended_oscillator_portfolio],
        'targets':[path.join(MODEL_PATH, 'Detrended Oscillator Portfolio-' + str(last_month_end()) + '.xlsx' )]
    }