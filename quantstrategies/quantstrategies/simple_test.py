#...
from datamanager import load
from quantstrategies.strategies.strategy import *
from quantstrategies.transforms import mean, momentum, log_returns, index_log_returns, movavg, max
from functools import partial

short_movavg = partial(movavg, period=20)
long_movavg = partial(movavg, period=50)
max20 = partial(max, period = 20)

price_close = load.load_close()
datan = SourceNode(price_close.ix[-100:])
reporter = SinkNode(name = 'StatsReport')
do_stats = datan.filter(load.get_all_listed()).transform(log_returns).transform(index_log_returns).stats(movavg20 = short_movavg, movavg50 = long_movavg, max = max)
stats = datan.stats(momentum = momentum, mean = mean).to_(reporter)

reporter.report()