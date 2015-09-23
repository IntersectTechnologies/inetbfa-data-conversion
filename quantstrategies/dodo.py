# Copyright 2015 Intersect Technologies CC
# 

from os import path
import datetime as dt

from datamanager.envs import *
from quantstrategies.strategies.model_portfolio import ModelPortfolio
import quantstrategies.strategies.nwu_momentum as nm
import quantstrategies.strategies.growth_portfolio as gp
from core.utils import last_month_end

enddt = last_month_end()
tmpd = enddt - dt.timedelta(days=365)
startdt = dt.date(tmpd.year, tmpd.month+1, 1)

def update_nwu_momentum_portfolio(dependencies, targets):
    nwu_momentum = ModelPortfolio(startdt, enddt, nm.fields())
    nwu_momentum.handle(nm.filter, nm.transform, nm.security_selection, nm.portfolio_selection)
    nwu_momentum.save(targets[0])

def update_growth_portfolio(dependencies, targets):
    growth = ModelPortfolio(startdt, enddt, gp.fields())
    growth.handle(gp.filter, gp.transform, gp.security_selection, gp.portfolio_selection)
    growth.save(targets[0])

def update_detrended_oscillator_portfolio(dependencies, targets):
    do = ModelPortfolio(startdt, enddt, gp.fields())
    do.handle(gp.filter, gp.transform, gp.security_selection, gp.portfolio_selection)
    do.save(targets[0])
   
def task_model_momentum_portfolio():
    return {
        'actions':[update_nwu_momentum_portfolio],
        'targets':[path.join(MODEL_PATH, 'NWU Momentum Portfolio-' + str(last_month_end()) + '.xlsx' )]
    }
    
def task_model_growth_portfolio():
    return {
        'actions':[update_growth_portfolio],
        'targets':[path.join(MODEL_PATH, 'Growth Portfolio-' + str(last_month_end()) + '.xlsx' )]
    }

def task_model_detrended_oscillator_portfolio():
    return {
        'actions':[update_detrended_oscillator_portfolio],
        'targets':[path.join(MODEL_PATH, 'Detrended Oscillator Portfolio-' + str(last_month_end()) + '.xlsx' )]
    }

def task_model_history():
    return {
    }

def task_model_transaction():
    return {
    }

def task_transaction_history():
    return {
    }

def task_portfolio_history():
    return {
    }

def task_indices():
    return {
    }