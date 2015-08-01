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

'''
This module contains a collection of models that are the core of a trading/portfolio management algorithm

A model takes transforms and raw price and financial data as inputs and calculates a signal or score for each security

Returns a dataframe

rows - tickers
cols - signals / scores

'''