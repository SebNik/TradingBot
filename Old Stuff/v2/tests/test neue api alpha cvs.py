from alpha_vantage.timeseries import TimeSeries
import csv
ts = TimeSeries(key='YOUR_API_KEY',output_format='csv')
data = ts.get_intraday(symbol='AAPL',interval='1min', outputsize='compact')
print(list(data))
for row in data:
    print(row)