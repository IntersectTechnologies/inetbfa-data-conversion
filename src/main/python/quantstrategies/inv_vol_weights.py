# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 16:47:26 2015

@author: Niel
"""
import bt
# fetch some data
data = bt.get('spy,agg,ibm', start='2010-01-01')
print data.head()

# create our new strategy
strategy2 = bt.Strategy('s2', [bt.algos.RunWeekly(),
                        bt.algos.SelectAll(),
                        bt.algos.WeighInvVol(),
                        bt.algos.Rebalance()])

# now let's test it with the same data set. We will also compare it with our first backtest.
test2 = bt.Backtest(strategy2, data)
res2 = bt.run(test2)

res2.plot()

res2.display()
res2.plot_security_weights()