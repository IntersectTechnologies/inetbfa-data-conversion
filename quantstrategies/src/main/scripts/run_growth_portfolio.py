import calendar as cal
from quantstrategies.growth_portfolio import *
import datetime as dt
import datamanager.datamodel as dm

td = dt.datetime.today()
enddt = dt.date(td.year, td.month-1, cal.monthrange(td.year, td.month-1)[1])
tmpd = enddt - dt.timedelta(days=365)
startdt = dt.date(tmpd.year, tmpd.month+1, 1)

mom = Momentum(startdt, enddt)
mom.save()