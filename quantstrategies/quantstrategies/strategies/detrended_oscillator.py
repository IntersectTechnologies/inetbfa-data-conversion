from os import path, listdir, makedirs
import pandas as pd
import numpy as np

import datetime as dt
import datamanager.datamodel as dm
from datamanager.datamodel import MarketData
from datamanager.envs import *
from quantstrategies.universe_selection import greater_than_filter, less_than_filter, top_filter
from quantstrategies.strategies.model_portfolio import ModelPortfolio
# Load the data

class DetrendedOscillator(ModelPortfolio):
	
	
	def __init(self, start_date, end_date):
		super(GrowthPortfolio, self).__init__(start_date, end_date)
		
	def run(self):
		'''
		'''
		