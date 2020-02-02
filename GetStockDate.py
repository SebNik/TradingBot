def get_data_intraday(symbol,interval,outputsize,API_KEY,savingtoCsv=True):
    from alpha_vantage.timeseries import TimeSeries
    import csv

    ts = TimeSeries(key=API_KEY,output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol,interval=interval, outputsize=outputsize)
    if savingtoCsv:
        data.to_csv('/home/niklas/Desktop/TradingBot/StockData/' + 'StockData-' + symbol + '-' + interval +'.csv')
    return data,meta_data

if __name__ == "__main__":
    API_KEY = 'U5C8JI4ELG45JNT7'
    symbol='MSFT'
    interval='1min'
    outputsize='compact'
    data,meta_data=get_data_intraday(symbol,interval,outputsize,API_KEY)
    print(data.head())