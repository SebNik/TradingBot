from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
ts = TimeSeries(key='YOUR_API_KEY',output_format='pandas')
data, meta_data = ts.get_intraday(symbol='TSE:TD',interval='1min', outputsize='full')
print(data)
data['4. close'].plot()
plt.title('Intraday TimeSeries Google')
plt.show()