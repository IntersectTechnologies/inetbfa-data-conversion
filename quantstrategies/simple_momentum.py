# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 17:22:11 2015

@author: Niel
"""

import bt
import quantifid as qd
import pandas as pd

start = pd.Timestamp('2010-01-04')
end = pd.Timestamp('2013-12-31')

# fetch some data
equities = qd.load_equities()
listed = qd.get_all_listed(equities)
active = qd.get_all_active(equities)
ords = qd.get_ordinaries(equities)

mc = qd.load_marketcap()
big_mc = qd.get_largest_marketcap(mc, 200, start)

# get union of active and listed equities
tickers = listed.intersection(active).intersection(ords).intersection(big_mc)

data = qd.load_prices(tickers, start=start, end=end)
big_prc = qd.get_larger_than_price(data, 100, start)
tickers = tickers.intersection(big_prc)

tickers = tickers[~tickers.isin(['EPS'])]

fdata = qd.load_prices(tickers, start=start, end=end)

# create the strategy
strategy1 = bt.Strategy('Momentum', [bt.algos.RunMonthly(),
                                     bt.algos.SelectHasData(pd.DateOffset(months=6)),
                                    bt.algos.StatTotalReturn(lookback=pd.DateOffset(months=12)),
                                    bt.algos.SelectN(20),
                                    bt.algos.WeighEqually(),
                                    bt.algos.Rebalance()])

# create a backtest and run it
test = bt.Backtest(strategy1, fdata)
#res = bt.run(test)

# first let's see an equity curve
#res.plot()
#
## ok and what about some stats?
#res.display()

# ok and how does the return distribution look like?

# create our new strategy
strategy2 = bt.Strategy('Random', [bt.algos.RunMonthly(),
                       bt.algos.SelectAll(pd.DateOffset(months=6)),
                        bt.algos.SelectRandomly(20),
                       bt.algos.WeighEqually(),
                       bt.algos.Rebalance()])
                       
test2 = bt.Backtest(strategy2, fdata)

strategy3 = bt.Strategy('AllEqual', [bt.algos.RunMonthly(),
                       bt.algos.SelectHasData(pd.DateOffset(months=6)),
                       bt.algos.WeighEqually(),
                       bt.algos.Rebalance()])

test3 = bt.Backtest(strategy3, fdata)                       
# now let's test it with the same data set. We will also compare it with our first backtest.


res = bt.run(test, test2, test3)

res.plot()

res.display()
res.plot_histogram()

# and just to make sure everything went along as planned, let's plot the security weights over time