# Copyright 2015 Intersect Technologies CC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import path
from datamanager.datamodel import MarketData
from datamanager.envs import *
import pandas as pd

class ModelPortfolio(object):
    '''
    '''
    
    def __init__(self, start_date, end_date, fields):
        '''
        '''
        self.start_date = start_date
        self.end_date = end_date

        daily_path = path.join(DATA_PATH, 'jse', 'equities', 'daily')
        self.data = pd.Panel(MarketData.load_from_file(daily_path, fields, start_date, end_date))

        assert type(self.data) == pd.Panel

    def handle(self, filter, transform, security_selection, portfolio_selection):
        '''
        Run the strategy
        '''
        # Filter the universe
        shares = filter(self.data)

        # Calculate the transforms - panel data
        trans = transform(self.data[shares])

        # Select the securities
        portf_input = security_selection(trans)

        # Create the portfolio
        self.output = portfolio_selection(portf_input)

    def save(self, fpath):
        self.output.to_excel(fpath)