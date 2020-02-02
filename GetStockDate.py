def get_data_intraday(API_KEY,symbol,interval,outputsize,savingtoCsv=True):
    from alpha_vantage.timeseries import TimeSeries

    ts = TimeSeries(key=API_KEY,output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol,interval=interval, outputsize=outputsize)
    if savingtoCsv:
        data.to_csv('/home/niklas/Desktop/TradingBot/StockData/' + 'StockData-' + symbol + '-' + interval +'.csv',sep=';')
    return data,meta_data

def get_data_latest(API_KEY,symbol,savingtoCsv=False):
    from alpha_vantage.timeseries import TimeSeries

    ts = TimeSeries(key=API_KEY,output_format='pandas')
    data = ts.get_quote_endpoint(symbol=symbol)
    return data

if __name__ == "__main__":
    API_KEY = 'U5C8JI4ELG45JNT7'
    symbol='MSFT'
    interval='1min'
    outputsize='compact'
    data,meta_data=get_data_intraday(API_KEY,symbol,interval,outputsize)
    print(data.head(2))
    print(get_data_latest(API_KEY,symbol))