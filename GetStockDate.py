from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

API_KEY = 'U5C8JI4ELG45JNT7'

ts = TimeSeries(key=API_KEY,output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
print(data)
data['4. close'].plot()
plt.title('Intraday TimeSeries Google')
plt.show()