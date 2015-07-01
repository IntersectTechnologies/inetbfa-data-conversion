#
# Copyright 2014 Intersect Technologies CC
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
import pandas as pd
import pytz

from datetime import datetime, timedelta
from dateutil import rrule
from functools import partial

start = pd.Timestamp('2005-01-01', tz='UTC')
end_base = pd.Timestamp('today', tz='UTC')

# Give an aggressive buffer for logic that needs to use the next trading
# day or minute.
end = end_base + timedelta(days=365)

def canonicalize_datetime(dt):
    # Strip out any HHMMSS or timezone info in the user's datetime, so that
    # all the datetimes we return will be 00:00:00 UTC.
    return datetime(dt.year, dt.month, dt.day, tzinfo=pytz.utc)


def get_non_trading_days(start, end):
	non_trading_rules = []

	start = canonicalize_datetime(start)
	end = canonicalize_datetime(end)
	
	# Weekends - Saturdays and Sundays of every week of the year
	weekends = rrule.rrule(
		rrule.YEARLY,
		byweekday=(rrule.SA, rrule.SU),
		cache=True,
		dtstart=start,
		until=end
	)
	non_trading_rules.append(weekends)
	
	# New Years's day - 1st day of the year
	new_years = rrule.rrule(
		rrule.MONTHLY,
		byyearday=1,
		cache=True,
		dtstart=start,
		until=end
	)
	non_trading_rules.append(new_years)
	
	# New Year's day on a Sunday
	new_years_sunday = rrule.rrule(
		rrule.MONTHLY,
		byyearday=2,
		byweekday=rrule.MO,
		cache=True,
		dtstart=start,
		until=end
	)
	non_trading_rules.append(new_years_sunday)
				
	# Human rights day 21 March
	hr_day = rrule.rrule(
		rrule.MONTHLY,
		bymonth=3,
		bymonthday=21,
		cache=True,
		dtstart=datetime(1996, 1, 1, tzinfo=pytz.utc),
		until=end
	)
	non_trading_rules.append(hr_day)
	
	# Human rights day on a Sunday - i.e. Monday will be the 22nd
	hr_sunday = rrule.rrule(
		rrule.MONTHLY,
		bymonth=3,
		bymonthday=22,
		byweekday=rrule.MO,
		cache=True,
		dtstart=datetime(1996, 1, 1, tzinfo=pytz.utc),
		until=end
	)
	non_trading_rules.append(hr_sunday)
	
	# US Good Friday rule
	good_friday = rrule.rrule(
		rrule.DAILY,
		byeaster=-2,
		cache=True,
		dtstart=start,
		until=end
	)
	non_trading_rules.append(good_friday)
	
	# Monday after Easter
	family_day = rrule.rrule(
		rrule.DAILY,
		byeaster=+1,
		cache=True,
		dtstart=start,
		until=end
	)
	non_trading_rules.append(family_day)

	# Freedom day - 27 April
	freedom_day = rrule.rrule(
		rrule.MONTHLY,
		bymonth=4,
		bymonthday=27,
		cache=True,
		dtstart=datetime(1994, 1, 1, tzinfo=pytz.utc),
		until=end
	)
	non_trading_rules.append(freedom_day)

	# Freedom day on a Sunday - i.e. Monday will be the 28th
	freedom_sunday = rrule.rrule(
		rrule.MONTHLY,
		bymonth=4,
		bymonthday=28,
		byweekday=rrule.MO,
		cache=True,
		dtstart=datetime(1994, 1, 1, tzinfo=pytz.utc),
		until=end
	)
	non_trading_rules.append(freedom_sunday)
	
	# Workers day - 1 May
	workers_day = rrule.rrule(
		rrule.MONTHLY,
		bymonth=5,
		bymonthday=1,
		cache=True,
		dtstart=datetime(1994, 1, 1, tzinfo=pytz.utc),
		until=end
	)
	non_trading_rules.append(workers_day)
	
	# Workers Sunday - 1 May
	workers_sunday = rrule.rrule(
		rrule.MONTHLY,
		bymonth=5,
		bymonthday=2,
		byweekday=rrule.MO,
		cache=True,
		dtstart=datetime(1994, 1, 1, tzinfo=pytz.utc),
		until=end
	)
	non_trading_rules.append(workers_sunday)

	# Youth Day
	youth_day = rrule.rrule(
		rrule.MONTHLY,
		bymonth=6,
		bymonthday=16,
		cache=True,
		dtstart=datetime(1995, 1, 1, tzinfo=pytz.utc),
		until=end
	)
	non_trading_rules.append(youth_day)

	# Youth Sunday
	youth_sunday = rrule.rrule(
		rrule.MONTHLY,
		bymonth=6,
		bymonthday=17,
		byweekday=rrule.MO,
		cache=True,
		dtstart=datetime(1995, 1, 1, tzinfo=pytz.utc),
		until=end
	)
	non_trading_rules.append(youth_sunday)
	
	# Womens Day
	womens_day = rrule.rrule(
		rrule.MONTHLY,
		bymonth=8,
		bymonthday=9,
		cache=True,
		dtstart=datetime(1995, 1, 1, tzinfo=pytz.utc),
		until=end
	)
	non_trading_rules.append(womens_day)
	
	# Womens Sunday
	womens_sunday = rrule.rrule(
		rrule.MONTHLY,
		bymonth=8,
		bymonthday=10,
		byweekday=rrule.MO,
		cache=True,
		dtstart=datetime(1995, 1, 1, tzinfo=pytz.utc),
		until=end
	)
	non_trading_rules.append(womens_sunday)
	
	# Heritage Day
	heritage_day = rrule.rrule(
		rrule.MONTHLY,
		bymonth=9,
		bymonthday=24,
		cache=True,
		dtstart=datetime(1995, 1, 1, tzinfo=pytz.utc),
		until=end
	)
	non_trading_rules.append(heritage_day)
		
	# Heritage Sunday
	heritage_sunday = rrule.rrule(
		rrule.MONTHLY,
		bymonth=9,
		bymonthday=25,
		byweekday=rrule.MO,
		cache=True,
		dtstart=datetime(1995, 1, 1, tzinfo=pytz.utc),
		until=end
	)
	non_trading_rules.append(heritage_sunday)
	
	# Reconcilliation Day - 16 December
	recon_day = rrule.rrule(
		rrule.MONTHLY,
		bymonth=12,
		bymonthday=16,
		cache=True,
		dtstart=start,
		until=end
	)
	non_trading_rules.append(recon_day)
	
	# Reconcilliation Sunday - 16 December
	recon_day = rrule.rrule(
		rrule.MONTHLY,
		bymonth=12,
		bymonthday=17,
		byweekday=rrule.MO,
		cache=True,
		dtstart=start,
		until=end
	)
	non_trading_rules.append(recon_day)
	
	christmas = rrule.rrule(
		rrule.MONTHLY,
		bymonth=12,
		bymonthday=25,
		cache=True,
		dtstart=start,
		until=end
	)
	non_trading_rules.append(christmas)
				
	# Day of Goodwill - 26th December
	goodwill = rrule.rrule(
		rrule.MONTHLY,
		bymonth=12,
		bymonthday=26,
		cache=True,
		dtstart=start,
		until=end
	)
	non_trading_rules.append(goodwill)
	
	# Day of Goodwill - 26th December
	goodwill_sunday = rrule.rrule(
		rrule.MONTHLY,
		bymonth=12,
		bymonthday=27,
		byweekday=rrule.MO,
		cache=True,
		dtstart=start,
		until=end
	)
	non_trading_rules.append(goodwill_sunday)
	
	non_trading_ruleset = rrule.rruleset()

	for rule in non_trading_rules:
		non_trading_ruleset.rrule(rule)

	non_trading_days = non_trading_ruleset.between(start, end, inc=True)
	
	########################################
	# Once-off holidays
	########################################
	# Add September 11th closings
	# http://en.wikipedia.org/wiki/Aftermath_of_the_September_11_attacks
	# Due to the terrorist attacks, the stock market did not open on 9/11/2001
	# It did not open again until 9/17/2001.
	#
	#    September 2001
	# Su Mo Tu We Th Fr Sa
	#                    1
	#  2  3  4  5  6  7  8
	#  9 10 11 12 13 14 15
	# 16 17 18 19 20 21 22
	# 23 24 25 26 27 28 29
	# 30

	for day_num in range(11, 17):
		non_trading_days.append(
			datetime(2001, 9, day_num, tzinfo=pytz.utc))

	
	# National and Local Government Elections
	# http://en.wikipedia.org/wiki/Public_holidays_in_South_Africa
	# 2 June 1999
	non_trading_days.append(datetime(1999, 6, 2, tzinfo=pytz.utc))
	# 14 April 2004
	non_trading_days.append(datetime(2004, 4, 14, tzinfo=pytz.utc))
	# 1 March 2006 - Local Government Elections
	non_trading_days.append(datetime(2006, 3, 1, tzinfo=pytz.utc))
	# 22 April 2009 
	non_trading_days.append(datetime(2009, 4, 22, tzinfo=pytz.utc))
	# 18 May 2008 - Local Government Elections
	non_trading_days.append(datetime(2011, 5, 18, tzinfo=pytz.utc))
	# 7 May 2014 - Local Government Elections
	non_trading_days.append(datetime(2014, 5, 7, tzinfo=pytz.utc))
	
	# Misc public holidays
	# http://en.wikipedia.org/wiki/Public_holidays_in_South_Africa
	# 
	
	# Y2K changeover
	non_trading_days.append(datetime(1999, 12, 31, tzinfo=pytz.utc))
	non_trading_days.append(datetime(2000, 1, 2, tzinfo=pytz.utc))
	
	# Human Rights day and Good Friday fell on the same day
	non_trading_days.append(datetime(2008, 5, 2, tzinfo=pytz.utc))
	
	# 27 December 2011 was declared a holiday by (acting) 
	# president Kgalema Motlanthe as Christmas Day fell on a Sunday 
	# which generally makes the following Monday a public holiday. 
	# However the following Monday the 26 December 2011 was the Day of Goodwill 
	# and therefore decreased the number of paid public holidays for the year. 
	# Initially this day was not to be declared a public holiday[16] but 
	# in mid-December the decision was changed
	non_trading_days.append(datetime(2011, 12, 27, tzinfo=pytz.utc))
	
	non_trading_days.sort()
	return pd.DatetimeIndex(non_trading_days)

non_trading_days = get_non_trading_days(start, end)
trading_day = pd.tseries.offsets.CDay(holidays=non_trading_days)


def get_trading_days(start, end, trading_day=trading_day):
	return pd.date_range(start=start.date(),
						 end=end.date(),
                         freq=trading_day).tz_localize('UTC')

trading_days = get_trading_days(start, end)


def get_early_closes(start, end):
	# 1:00 PM close rules based on
	# http://quant.stackexchange.com/questions/4083/nyse-early-close-rules-july-4th-and-dec-25th # noqa
	# and verified against http://www.nyse.com/pdfs/closings.pdf

	# These rules are valid starting in 1995

	start = canonicalize_datetime(start)
	end = canonicalize_datetime(end)

	start = max(start, datetime(1995, 1, 1, tzinfo=pytz.utc))
	end = max(end, datetime(1995, 1, 1, tzinfo=pytz.utc))

	# Not included here are early closes prior to 1993
	# or unplanned early closes

	early_close_rules = []

	christmas_eve = rrule.rrule(
		rrule.MONTHLY,
		bymonth=12,
		bymonthday=24,
		byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH),
		cache=True,
		dtstart=start,
		until=end
	)
	early_close_rules.append(christmas_eve)

	new_years_eve = rrule.rrule(
		rrule.MONTHLY,
		bymonth=12,
		bymonthday=31,
		byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH),
		cache=True,
		dtstart=start,
		until=end
	)
	early_close_rules.append(new_years_eve)
	
	early_close_ruleset = rrule.rruleset()

	for rule in early_close_rules:
		early_close_ruleset.rrule(rule)
	early_closes = early_close_ruleset.between(start, end, inc=True)

	early_closes.sort()
	return pd.DatetimeIndex(early_closes)

early_closes = get_early_closes(start, end)


def get_open_and_close(day, early_closes):
	market_open = pd.Timestamp(
		datetime(
			year=day.year,
			month=day.month,
			day=day.day,
			hour=9,
			minute=31),
		tz='US/Eastern').tz_convert('UTC')
	# 1 PM if early close, 4 PM otherwise
	close_hour = 13 if day in early_closes else 16
	market_close = pd.Timestamp(
		datetime(
			year=day.year,
			month=day.month,
			day=day.day,
			hour=close_hour),
		tz='US/Eastern').tz_convert('UTC')

	return market_open, market_close


def get_open_and_closes(trading_days, early_closes):
	open_and_closes = pd.DataFrame(index=trading_days,
								   columns=('market_open', 'market_close'))

	get_o_and_c = partial(get_open_and_close, early_closes=early_closes)

	open_and_closes['market_open'], open_and_closes['market_close'] = \
		zip(*open_and_closes.index.map(get_o_and_c))

	return open_and_closes

open_and_closes = get_open_and_closes(trading_days, early_closes)

