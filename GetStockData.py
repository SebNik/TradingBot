# this code is reading the stock data
# all data is from GMT-5 -> Time Germany -6
def api_key_finder():
    # selects the right api key for maximal success
    from time import gmtime, strftime
    import os
    import sqlite3
    # 500 requests a day -- 5 per min

    file_api = '/home/niklas/Desktop/TradingBot/api-key_logs.db'
    if not os.path.isfile(file_api):
        conn = sqlite3.connect(file_api)
        c = conn.cursor()
        c.execute('CREATE TABLE ApiKeyLog (id INTEGER, date TEXT, ApiKeyNo TEXT, ApiKey TEXT)')
    else:
        conn = sqlite3.connect(file_api)
        c = conn.cursor()

    api_keys = ['U5C8JI4ELG45JNT7', 'L7C6HSQARL8LR5E4', 'D7TUJ5FRXFV44XPO', '2EGXAE0H594DZ9U5', 'UNK3NBPC8S27EKHN',
                'ZX686301JW1AMF8I', 'DI2GYUJXWL8OL030']
    selected_api_key = ''
    # date TEXT, api-key-no INTEGER, api-key TEXT, counter INTEGER
    # %Y+%m+%d-%A+%H:%M:%S APIKEYNO APIKEY counter
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
    # ideal call time is resolution_data
    time = strftime("%Y+%m+%d-%A+%H:%M:%S", gmtime())
    time_day = strftime("%Y+%m+%d", gmtime())
    # getting data from sqlite3
    c.execute("SELECT * FROM ApiKeyLog ORDER BY id DESC LIMIT 1")
    last_line = c.fetchone()
    # prepare the last line for checking
    if last_line is not None:
        out = [item for item in last_line]
        last_api_key_log = [out[1].split('-')[0], out[1].split('-')[1], out[2], out[3], out[0]]
    # check if nothing is in the database and check the
    if last_line is None:
        from random import randint
        no = randint(0, len(api_keys) - 1)
        selected_api_key = api_keys[no]
        c.execute("INSERT INTO ApiKeyLog VALUES (0,?,?,?)", (time, str(no), selected_api_key))
        conn.commit()
    # starting to check
    if last_api_key_log[0] == time_day:
        if api_keys[int(last_api_key_log[2])] == last_api_key_log[3]:
            no = int(last_api_key_log[2]) + 1
            if no == len(api_keys):
                no = 0
            selected_api_key = api_keys[no]
            c.execute("INSERT INTO ApiKeyLog VALUES (?,?,?,?)",
                      (int(last_api_key_log[4]) + 1, time, str(no), selected_api_key))
            conn.commit()
    conn.close()
    # closing and saving file
    return selected_api_key, str(resolution_data)


def get_data_intraday(symbol, interval, outputsize, savingtoCsv=False):
    # gets data over a periode of a day
    from alpha_vantage.timeseries import TimeSeries
    from time import gmtime, strftime
    import sqlite3
    import os
    # loading stock prices
    # getting the right api key
    API_KEY, waiting_times = api_key_finder()
    print(API_KEY)
    # setting the reading data
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    # reading the right time
    time = strftime("%Y-%m-%d-%A", gmtime())
    # geting the final data
    data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
    # check if need to save to CSV-File
    if savingtoCsv:
        data.to_csv(
            '/home/niklas/Desktop/TradingBot/StockData/' + 'StockData-' + symbol + '-' + interval + '-' + time + '.csv',
            sep=';')
        # saved data csv-file data
    # time for loading the database
    file = '/home/niklas/Desktop/TradingBot/StockData/StockData-{}.db'.format(symbol)
    if not os.path.isfile(file):
        conn = sqlite3.connect(file)
        c = conn.cursor()
        sql = "INSERT INTO {} VALUES".format(x)
        c.execute(
            'CREATE TABLE IntraDay-{} (date1 TEXT, open2 REAL, high3 REAL, low4 REAL, close5 REAL, volume REAL)'.format(
                symbol + '-' + interval))
    else:
        conn = sqlite3.connect(file)
        c = conn.cursor()
    # now the database is connected through
    # next we are going to check if the table already exists
    tablename = 'IntraDay-{}'.format(symbol + '-' + interval)
    stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(tablename)
    c.execute(stmt)
    result = c.fetchone()
    if result:
        # table found
        None
    else:
        # table not found
        c.execute(
            'CREATE TABLE IntraDay-{} (date1 TEXT, open2 REAL, high3 REAL, low4 REAL, close5 REAL, volume REAL)'.format(
                symbol + '-' + interval))
    # reading data from database
    data = c.execute("SELECT * FROM {}".format(tablename))
    last_line_table = data[-1]
    # starting to insert data into table
    sql = "INSERT INTO {} VALUES".format(tablename)
    # last line None nothing in so putting new in
    data.to_sql(tablename, conn, if_exists="replace")

    return data, meta_data  # , waiting_times


def get_data_daily(symbol, outputsize, savingtoCsv=True):
    # gets data over of a day the daily open, daily high, daily low, daily close, daily volume
    # with full all data until 2000 is shown, with compact the last 100 days
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
    return data, meta_data  # , waiting_times


def get_data_weekly(symbol, savingtoCsv=True):
    # gets data over of a week
    # with full all data until 2000 is shown, with compact the last 100 days
    from alpha_vantage.timeseries import TimeSeries
    from time import gmtime, strftime
    # time for saving
    API_KEY, waiting_times = api_key_finder()
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    time = strftime("%Y-%m-%d-%A", gmtime())
    data, meta_data = ts.get_weekly(symbol=symbol)
    if savingtoCsv:
        data.to_csv(
            '/home/niklas/Desktop/TradingBot/StockData/' + 'StockData-Weekly-' + symbol + '-' + time + '.csv',
            sep=';')
        # saved data csv-file data
    return data, meta_data, waiting_times


def get_data_monthly(symbol, savingtoCsv=True):
    # gets data over of a week
    # with full all data until 2000 is shown, with compact the last 100 days
    from alpha_vantage.timeseries import TimeSeries
    from time import gmtime, strftime
    # time for saving
    API_KEY, waiting_times = api_key_finder()
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    time = strftime("%Y-%m-%d-%A", gmtime())
    data, meta_data = ts.get_monthly(symbol=symbol)
    if savingtoCsv:
        data.to_csv(
            '/home/niklas/Desktop/TradingBot/StockData/' + 'StockData-Monthly-' + symbol + '-' + time + '.csv',
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
    meta_data, data = get_data_intraday('AAPL', '1min', 'compact')
