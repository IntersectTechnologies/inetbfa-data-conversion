# -*- coding: utf-8 -*-
#
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

"""
Created on Tue Dec 09 11:41:51 2014

@author: Niel
"""

import zipline
from zipline.finance import trading
from zipline.utils import tradingcalendar_jse
from os import path, getcwd, listdir, makedirs
from os.path import expanduser
import json
import pandas as pd
from . import universe_select as us
from quantifi.load import load_equities, load_marketcap, load_panel

BACKTEST_PATH = path.join(
    expanduser("~"),
    '.zipline',
    'backtests'
)

EQUITIES = load_equities()
MARKETCAP = load_marketcap()

class Config(object):
    '''

    '''
    def __init__(self):
        self._version = (0,1)
        self._name = 'Test'
        self._output_dir = BACKTEST_PATH
        self._config = {}
        
        # Defaults
        self._config['exchange'] = 'JSE'
        self._load_config()

    def _load_config(self):
        '''
        '''

        fp = self.get_config_source_path()
        try:
            with open(fp, 'r') as f:
                config = json.load(f)
        except IOError:
            print 'Error reading config file, loading defaults...'
            quandl = {}
            quandl['source'] = 'NIELSWART'
            quandl['authtoken'] = 'MBaawgy9DEZJHU3NkcNd'
            
            config = {}
            config['name'] = 'Simple Momentum'
            config['version'] = 'latest'			
            config['start'] = '2008-1-1'
            config['end'] = '2013-12-31'
            config['source'] = 'quandl' 
            config['quandl'] = quandl
            
            config['symbols'] = ['SOL', 'NPN']
            config['metrics'] = ["Open", "High", "Low", "Close", "Volume", "Market Cap", "Total Number Of Shares", "Number Of Trades"]
            config['benchmark'] = 'J203' 
            config['timezone'] = "Africa/Johannesburg"
            
        self._name = config['name']
        self._version = self._parse_version(config['version'])
        self._config = config
        
        self._parse_symbols()
        
        self._output_dir = self._get_output_dir()
        if not path.exists(self._output_dir):
                print 'Creating new folder: ' + self._output_dir
                makedirs(self._output_dir)	
    
        with open(self.get_config_dest_path(), 'w') as f:
            json.dump(config, f, sort_keys=True, indent=4)

    def _validate(self):
        pass
    
    @property
    def version(self):
        return self._version
    
    @property	
    def name(self):
        return self._name
    
    @property	
    def module(self):
        return self._config['module']
    
    def pretty_version(self):
        '''
        '''
        return '{major}.{minor}'.format(major=self._version[0],
                minor=self._version[1])
                
    def _parse_version(self, version):
        '''
        '''
        
        if type(version) == str or type(version) == unicode:
            if version == 'latest':
                # look for latest version
                fp = path.join(getcwd(), 'strategies', self._name)
                versions = [f for f in listdir(fp) if path.isdir(f)]
                vt = [(v.split('.')[0], v.split('.')[1]) for v in versions]
                
                maxmajor = max([m[0] for m in vt])	
                minor = max([m[1] for m in vt if vt[0] == maxmajor])
                
                resolved = (maxmajor, minor)
            else:
                try:
                    resolved = (int(version.split('.')[0]),int(version.split('.')[1]))
                except:
                    raise ValueError('The version can not be parsed...')
        return resolved
        
    def _parse_symbols(self):
        
        bm = self._config['benchmark']
        symbols = self._config['symbols']
        if '_' not in bm:
            bm = self._config['exchange'] + '_' + bm
        syms = []
        
        parsed_syms = symbols.lower().replace(' ', '')
        if type(symbols)!=list:
            if parsed_syms == 'top40':
                symbols = us.get_largest_marketcap(40, MARKETCAP)
            elif symbols.lower().split(' ')[0] == 'top':
                n = int(symbols.lower().split(' ')[1])
                symbols = us.get_largest_marketcap(n, MARKETCAP)
            elif parsed_syms == 'all':
                symbols = us.get_all(EQUITIES)
            elif parsed_syms == 'ordinary' or parsed_syms == 'ordinaries':
                symbols = us.get_ordinaries(EQUITIES)
            else:
                raise ValueError('The symbols description can not be parsed...')
            
        for s in symbols:
            if '_' not in s:
                s = self._config['exchange'] + '_' + s
                syms.append(s)
                
        self._config['benchmark'] = bm
        self._config['symbols'] = syms
            
                    
    def get_config_source_path(self):
        '''
        '''
                
        return path.join(getcwd(), 'config.json')
    
    def get_config_dest_path(self):
        '''
        '''
        return path.join(self._output_dir, 'config.json')
        
        
    def _get_output_dir(self):
        
        pathname = 	"{name}_v{major}.{minor}-{date}".format(
                    name=self._name,
                    major=self._version[0],
                    minor=self._version[1],
                    date=pd.Timestamp('now')).replace(':', '-')
                    
        return path.join(BACKTEST_PATH, pathname)			
    
    
    
    def get_output_path(self):
        '''
        '''
        
        return path.join(self._output_dir, 'performance.csv')
    
    def load_data(self):
        '''
        '''
        # parse arguments
        start = pd.Timestamp(self._config['start'], tz='UTC')
        end = pd.Timestamp(self._config['end'], tz='UTC')
        symbols = self._config['symbols']
        
        if self._config['source'] == 'quandl':
            quandl = self._config['quandl']
            data = zipline.data2.load_bars_from_quandl(source=quandl['source'],
                stocks=symbols, start=start, end=end, authtoken=quandl['authtoken'])    
                
        elif (self._config['source'] == 'local' or self._config['source'] == 'file'):
            data = load_panel(self._config['metrics'])
        else:     
            raise NotImplementedError(
                'Source %s not implemented.' % self._config['source'])
        return data
    
    def initialize_environment(self):
        '''
        '''
    
        if self._config['source'] == 'quandl':
            quandl = self._config['quandl']
            env = trading.TradingEnvironment(bm_symbol=self._config['benchmark'],
                    exchange_tz=self._config['timezone'], 
                    env_trading_calendar=tradingcalendar_jse,
                    source=quandl['source'],
                    authtoken=quandl['authtoken'])
                    
            return env
        elif self._config['source'] == 'local':
            quandl = self._config['quandl']
            env = trading.TradingEnvironment(bm_symbol=self._config['benchmark'],
                    exchange_tz=self._config['timezone'], 
                    env_trading_calendar=tradingcalendar_jse,
                    source='local',
                    authtoken=quandl['authtoken'])
            return env

