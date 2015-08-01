# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 09:30:10 2014

@author: Niel
"""
import pandas as pd


source = '../data/'
dest = '../datamanager/'
# Transform ratios data from sql-like table storage to matrix-like datastructure with dates as rows and tickers as columns

# Read ratios file
ratios = pd.read_csv('../data/jse/ratios/jseratios.csv')

# Extract book-to-market and save as csv file
booktomarket = ratios.pivot(index='datestamp', columns='ticker', values='booktomarket')
booktomarket.to_csv('../datamanager/jse/ratios/monthly/' + 'book2market.csv', sep=',')

pe = ratios.pivot(index='datestamp', columns='ticker', values='pricetoearnings')
pe.to_csv(dest + 'jse/ratios/monthly/' + 'pe.csv', sep=',')

dy = ratios.pivot(index='datestamp', columns='ticker', values='dividendyield')
dy.to_csv(dest + 'jse/ratios/monthly/' + 'dy.csv', sep=',')

ey = ratios.pivot(index='datestamp', columns='ticker', values='earningsyield')
ey.to_csv(dest + 'jse/ratios/monthly/' + 'ey.csv', sep=',')


jseclose = pd.read_csv('../data/jsecloseprice.csv')

daily_close = jseclose.pivot(index='price_date', columns='ticker', values='price_close')
daily_close.to_csv(dest + 'jse/market/daily/'+ 'close.csv')

# Get tickers for each id
equities = pd.read_csv('../data/equities.csv', index_col = 0)
exchanges = pd.read_csv('../data/exchanges.csv', index_col = 0)

# first add exchange code to equities table by joining on exchange_id
equities.join(exchanges, on='exchange_id').to_csv('../datamanager/jse/equities.csv')

# get all equity price data

# get all jse data
jseprices = pd.read_csv('../data/jseprices.csv')

# transform and save open
daily_open = jseprices.pivot(index='price_date', columns='ticker', values='price_open')
daily_open.to_csv(dest + 'jse/market/daily/open.csv')

daily_high = jseprices.pivot(index='price_date', columns='ticker', values='price_high')
daily_high.to_csv(dest + 'jse/market/daily/high.csv')

daily_low = jseprices.pivot(index='price_date', columns='ticker', values='price_low')
daily_low.to_csv(dest + 'jse/market/daily/low.csv')

daily_volume = jseprices.pivot(index='price_date', columns='ticker', values='volume')
daily_volume.to_csv(dest + 'jse/market/daily/volume.csv')

daily_shares_issued = jseprices.pivot(index='price_date', columns='ticker', values='shares_issued')
daily_shares_issued.to_csv(dest + 'jse/market/daily/shares_issued.csv')

daily_vwap = jseprices.pivot(index='price_date', columns='ticker', values='vwap')
daily_vwap.to_csv(dest + 'jse/market/daily/vwap.csv')

daily_ey = jseprices.pivot(index='price_date', columns='ticker', values='ey')
daily_ey.to_csv(dest + 'jse/ratios/daily/ey.csv')

daily_dy = jseprices.pivot(index='price_date', columns='ticker', values='dy')
daily_dy.to_csv(dest + 'jse/ratios/daily/dy.csv')

# Read new data and combine into single file
jse_a1 = pd.read_csv('../data/jse/market/daily/jse_a1.csv')
jse_a2 = pd.read_csv('../data/jse/market/daily/jse_a2.csv')
jse_a = jse_a1.append(jse_a2)

jse_b = pd.read_csv('../data/jse/market/daily/jse_b.csv')
jse_ab = jse_a.append(jse_b)

jse_c = pd.read_csv('../data/jse/market/daily/jse_c.csv')
jse_ac = jse_ab.append(jse_c)

jse_d = pd.read_csv('../data/jse/market/daily/jse_d.csv')
jse_ad = jse_ac.append(jse_d)

jse_e = pd.read_csv('../data/jse/market/daily/jse_e.csv')
jse_ae = jse_ad.append(jse_e)

jse_f = pd.read_csv('../data/jse/market/daily/jse_f.csv')
jse_af = jse_ae.append(jse_f)

jse_h = pd.read_csv('../data/jse/market/daily/jse_h.csv')
jse_ah = jse_af.append(jse_h)

jse_i = pd.read_csv('../data/jse/market/daily/jse_i.csv')
jse_ai = jse_ah.append(jse_i)

jse_j = pd.read_csv('../data/jse/market/daily/jse_j.csv')
jse_aj = jse_ai.append(jse_j)

jse_k = pd.read_csv('../data/jse/market/daily/jse_k.csv')
jse_ak = jse_aj.append(jse_k)

jse_l = pd.read_csv('../data/jse/market/daily/jse_l.csv')
jse_al = jse_ak.append(jse_l)

jse_uv = pd.read_csv('../data/jse/market/daily/jse_uv.csv')
jse_av = jse_al.append(jse_uv)

jse_w = pd.read_csv('../data/jse/market/daily/jse_w.csv')
jse_aw = jse_av.append(jse_w)

jse_aw.to_csv('../data/jse/market/daily/jse_all.csv',index=False)

# Now read new file and transform and save
jse_new = pd.read_csv('../data/jse/market/daily/jse_all.csv')
jse_new.drop_duplicates(cols= ['Date', 'Ticker'], inplace=True)

jse_new.to_csv('../data/jse/market/daily/jse_all.csv', index=False)

daily_close_new = jse_new.pivot(index='Date', columns='Ticker', values='Close')
daily_close_new.to_csv('../datamanager/jse/market/daily/new/close.csv')

daily_open_new = jse_new.pivot(index='Date', columns='Ticker', values='Open')
daily_open_new.to_csv('../datamanager/jse/market/daily/new/open.csv')

daily_high_new = jse_new.pivot(index='Date', columns='Ticker', values='High')
daily_high_new.to_csv('../datamanager/jse/market/daily/new/high.csv')

daily_low_new = jse_new.pivot(index='Date', columns='Ticker', values='Low')
daily_low_new.to_csv('../datamanager/jse/market/daily/new/low.csv')

daily_volume_new = jse_new.pivot(index='Date', columns='Ticker', values='Volume')
daily_volume_new.to_csv('../datamanager/jse/market/daily/new/volume.csv')

daily_vwap_new = jse_new.pivot(index='Date', columns='Ticker', values='VWAP')
daily_vwap_new.to_csv('../datamanager/jse/market/daily/new/vwap.csv')

daily_shares_new = jse_new.pivot(index='Date', columns='Ticker', values='Total Number Of Shares')
daily_shares_new.to_csv('../datamanager/jse/market/daily/new/shares_issued.csv')

daily_dy_new = jse_new.pivot(index='Date', columns='Ticker', values='DY')
daily_dy_new.to_csv('../datamanager/jse/ratios/daily/new/dy.csv')

daily_ey_new = jse_new.pivot(index='Date', columns='Ticker', values='EY')
daily_ey_new.to_csv('../datamanager/jse/ratios/daily/new/ey.csv')

# merge old and new daily market data



