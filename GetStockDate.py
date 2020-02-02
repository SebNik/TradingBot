from alpha_vantage.timeseries import TimeSeries
import csv
import pandas as pd

API_KEY = 'U5C8JI4ELG45JNT7'
symbol='MSFT'
interval='1min'
outputsize='compact'

ts = TimeSeries(key=API_KEY,output_format='pandas')
data, meta_data = ts.get_intraday(symbol=symbol,interval=interval, outputsize=outputsize)

print(data.head())
data.to_csv('/home/niklas/Desktop/TradingBot/StockData/' + 'StockData-' + symbol + '-' + interval +'.csv')