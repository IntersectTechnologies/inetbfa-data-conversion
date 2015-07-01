# to see our plots
# %pylab inline

import bt
from quantifi.load import load_prices
# fetch some data

#data = bt.get('spy,agg,ibm', start='2010-01-01')

tickers = ['SAB', 'SOL', 'NPN', 'SLM', 'FSR', 'PSG', 'AGL', 'BIL', 'SBK', 'CPI']

data = load_prices(tickers, start='2010-01-04', end='2013-12-31')

print data.head()

# create the strategy
strategy1 = bt.Strategy('Equal', [bt.algos.RunMonthly(),
                       bt.algos.SelectHasData(),
                       bt.algos.WeighEqually(),
                       bt.algos.Rebalance()])

# create a backtest and run it
test = bt.Backtest(strategy1, data)
#res = bt.run(test)

# first let's see an equity curve
#res.plot()
#
## ok and what about some stats?
#res.display()

# ok and how does the return distribution look like?


# create our new strategy
strategy2 = bt.Strategy('MeanVar', [bt.algos.RunQuarterly(),
                       bt.algos.SelectHasData(),
                       bt.algos.WeighMeanVar(),
                       bt.algos.run_always(bt.algos.RebalanceOverTime())])

# now let's test it with the same data set. We will also compare it with our first backtest.
test2 = bt.Backtest(strategy2, data)
res2 = bt.run(test, test2)

res2.plot()

res2.display()
res2.plot_histogram()

# and just to make sure everything went along as planned, let's plot the security weights over time
res2.plot_security_weights(1)