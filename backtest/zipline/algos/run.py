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
Created on Tue Dec 09 11:59:41 2014

@author: Niel
"""
import importlib
import sys
import zipline

from utils.algo_config import Config

def main():
    """
    """
    
    config = Config()
    name = config.name
    version = config.version
    mod = config.module
    m = importlib.import_module('strategies.' + mod)

    # Algo arguments
    data = config.load_data()
    exchange = config.initialize_environment()

    with exchange:
        algo = zipline.TradingAlgorithm(initialize=m.initialize, handle_data=m.handle_data, analyze=m.analyze)
        print 'Simulating strategy {name} version {major}.{minor}...'.format(
                name = name,
                major = version[0],
                minor = version[1])
        perf = algo.run(data)
        perf.to_csv(config.get_output_path(), sep=',')
	
if __name__ == "__main__":    
    main()
    sys.exit(0)