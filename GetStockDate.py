# all data is from GMT-5 -> Time Germany -6
def api_key_finder():
    # selects the right api key for maximal success
    from time import gmtime, strftime
    import os
    # 500 requests a day -- 5 per min
    file_api = 'api-key_logs.txt'
    api_keys = ['U5C8JI4ELG45JNT7', 'L7C6HSQARL8LR5E4', 'D7TUJ5FRXFV44XPO', '2EGXAE0H594DZ9U5', 'UNK3NBPC8S27EKHN',
                'ZX686301JW1AMF8I', 'DI2GYUJXWL8OL030']
    selected_api_key = ''
    # log format:%Y+%m+%d-%A+%H:%M:%S-APIKEYNO-APIKEY-requests
    closing_sec = 16 * 60 * 60
    trading_sec = closing_sec - (((int(strftime("%H", gmtime())) - 5) * 60) + int(strftime("%M", gmtime()))) * 60
    # how many seconds are left for the day in trading
    resolution_data = (trading_sec / 500) / len(api_keys)
    # print(resolution_data)
    # gives how many seconds are between possible requests
    calls_per_key_per_min = 60 / resolution_data * len(api_keys)
    if calls_per_key_per_min < 6:
        # not possible
        while calls_per_key_per_min < 6:
            calls_per_key_per_min = 60 / resolution_data * len(api_keys)
            resolution_data += 0.25
    # ideal call time is resoulution_data
    if not os.path.isfile(file_api):
        f = open(file_api, 'x')
        f.write('-Logs of APIs-\n')
        f.close()
    f = open(file_api, 'r')
    api_key_logs = f.readlines()
    last_api_key_log = api_key_logs[-1].split('-')
    f.close()
    time = strftime("%Y+%m+%d-%A+%H:%M:%S", gmtime())
    time_day = strftime("%Y+%m+%d", gmtime())
    # opens for logging
    f = open(file_api, 'a')
    # starting to check
    if last_api_key_log[0] == time_day:
        if api_keys[int(last_api_key_log[2])] == last_api_key_log[3]:
            no = int(last_api_key_log[2]) + 1
            if no == len(api_keys):
                no = 0
            selected_api_key = api_keys[no]
            f.write(time + '-' + str(no) + '-' + selected_api_key + '-' + str(int(last_api_key_log[4]) + 1) + '\n')
    else:
        from random import randint
        no = randint(0, len(api_keys) - 1)
        selected_api_key = api_keys[no]
        f.write(time + '-' + str(no) + '-' + selected_api_key + '-' + '0' + '\n')
    f.close()
    # closing and saving file
    return selected_api_key, str(resolution_data)


def get_data_intraday(symbol, interval, outputsize, savingtoCsv=True):
    # gets data over a periode of a day
    from alpha_vantage.timeseries import TimeSeries
    from time import gmtime, strftime
    # time for saving
    API_KEY, waiting_times = api_key_finder()
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    time = strftime("%Y-%m-%d-%A", gmtime())
    data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
    if savingtoCsv:
        data.to_csv(
            '/home/niklas/Desktop/TradingBot/StockData/' + 'StockData-' + symbol + '-' + interval + '-' + time + '.csv',
            sep=';')
        # saved data csv-file data
    return data, meta_data, waiting_times

def get_data_daily(symbol, outputsize, savingtoCsv=True):
    # gets data over of a day the daily open, daily high, daily low, daily close, daily volume
    # with full all data until 2020 is shown, with compact the last 100 days
    from alpha_vantage.timeseries import TimeSeries
    from time import gmtime, strftime
    # time for saving
    API_KEY, waiting_times = api_key_finder()
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    time = strftime("%Y-%m-%d-%A", gmtime())
    data, meta_data = ts.get_daily(symbol=symbol, outputsize=outputsize)
    if savingtoCsv:
        data.to_csv(
            '/home/niklas/Desktop/TradingBot/StockData/' + 'StockData-Daily-' + symbol + '-' + outputsize + '-' + time + '.csv',
            sep=';')
        # saved data csv-file data
    return data, meta_data, waiting_times

def get_data_latest(symbol, savingtoCsv=False):
    # reads the latest data of the API
    # get changes of the last day
    from alpha_vantage.timeseries import TimeSeries
    API_KEY, waiting_times = api_key_finder()
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    data = ts.get_quote_endpoint(symbol=symbol)
    return data[0], waiting_times


if __name__ == "__main__":
    import time

    symbol = 'MSFT'
    interval = '1min'
    outputsize = 'compact'
    # for i in range(0, 10):
    #     data, meta_data, waiting_times = get_data_intraday(symbol, interval, outputsize)
    #     data_latest, waiting_times = get_data_latest(symbol)
    #     print(waiting_times)
    #     print(meta_data)
    #     print(data.head(1))
    #     print(data_latest['05. price'])
    #     time.sleep(5)
    data_daily, meta_data, waiting_times = get_data_daily(symbol, outputsize)
    print(data_daily.head())
