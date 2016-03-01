mkdir /c/root/data/converted/tickers
cd /c/root/intersect/datamanager
doit convert* swap
cd /c/root/data/converted/tickers
csvstack --filename -n tickers *.csv > all_jse_equity_data.csv