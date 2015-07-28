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
The security selection function takes a model as input and generates signals and scores used to select the securities to include in the portfolio

The security selection algorithm returns a list of security id's, positions and other data for each security needed in the portfolio selection algo

Returns a dataframe:

rows - security ids
cols - positions and other metrics

Example:
    Momentum:


    MACD:


    Pair Trading:

'''

def topn(model, ranking_var, n):
    ''' 
    Rank and select the top n securities on the ranking_var
    '''

