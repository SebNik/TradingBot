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
    else:
        from random import randint
        no = randint(0, len(api_keys) - 1)
        selected_api_key = api_keys[no]
        c.execute("INSERT INTO ApiKeyLog VALUES (0,?,?,?)", (time, str(no), selected_api_key))
        conn.commit()
    conn.close()
    # closing and saving file
    return selected_api_key, str(resolution_data)


def write_to_database(data, name, symbol, interval, savingtoCsv=False):
    # this function will write the stock data into the database
    # loading the needed modules
    import os
    import sqlite3
    import pandas as pd
    # time for loading the database
    file = '/home/niklas/Desktop/TradingBot/StockData/StockData-{}.db'.format(symbol)
    tablename = name + symbol + interval
    if not os.path.isfile(file):
        conn = sqlite3.connect(file)
        c = conn.cursor()
    else:
        conn = sqlite3.connect(file)
        c = conn.cursor()
    # now the database is connected through
    # next we are going to check if the table already exists
    table_check = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(tablename)
    c.execute(table_check)
    result = c.fetchone()
    # renamed data index
    data.rename(columns={'index': 'date'}, inplace=True)
    data.index.name = ' '
    if result:
        # table found
        # read data which is already in database
        df = pd.read_sql_query("SELECT * FROM {}".format(tablename), conn)  # , index_col='date')
        # print(df.head())
        # dataframes joined after each other
        new_df = pd.concat([data, df], ignore_index=True)
        # duplicates are removed
        new_df.drop_duplicates(subset='date', keep='last', inplace=True, ignore_index=True)
        # sorting dataframe by values
        new_df.sort_values('date', inplace=True, ascending=False)
        # print(new_df.head())
    else:
        # table not found
        new_df = data
    # check if need to save to CSV-File
    if savingtoCsv:
        # saved data csv-file data
        new_df.to_csv(
            '/home/niklas/Desktop/TradingBot/StockData/' + 'StockData-' + symbol + '-' + interval + '.csv',
            sep=';')
    # write data to database
    new_df.to_sql(tablename, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()


def get_data_intraday(symbol, interval, outputsize, savingtoCsv=False):
    # gets data over a period of a day
    # loading necessary modules
    from alpha_vantage.timeseries import TimeSeries
    # getting the right api key
    API_KEY, waiting_times = api_key_finder()
    # setting the reading data
    ts = TimeSeries(key=API_KEY, output_format='pandas', indexing_type='integer')
    # getting the final data
    data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
    # writing data to database and csv
    write_to_database(data, 'IntraDay', symbol, interval, savingtoCsv)

    return data, meta_data


def get_data_daily(symbol, outputsize, savingtoCsv=True):
    # gets data over of a day the daily open, daily high, daily low, daily close, daily volume
    # with full all data until 2000 is shown, with compact the last 100 days
    from alpha_vantage.timeseries import TimeSeries
    # time for collecting data
    # selecting api key
    API_KEY, waiting_times = api_key_finder()
    # creating nessary object
    ts = TimeSeries(key=API_KEY, output_format='pandas', indexing_type='integer')
    # reading data into daily
    data, meta_data = ts.get_daily(symbol=symbol, outputsize=outputsize)
    # writing data to database and csv
    write_to_database(data, 'Daily', symbol, 'daily', savingtoCsv)
    return data, meta_data


def get_data_weekly(symbol, savingtoCsv=True):
    # gets data over of a week
    # loading necessary modules
    from alpha_vantage.timeseries import TimeSeries
    # getting api key
    API_KEY, waiting_times = api_key_finder()
    # creating necessary object
    ts = TimeSeries(key=API_KEY, output_format='pandas', indexing_type='integer')
    # reading data into pandas
    data, meta_data = ts.get_weekly(symbol=symbol)
    # writing data to database and csv
    write_to_database(data, 'Weekly', symbol, 'weekly', savingtoCsv)
    return data, meta_data


def get_data_monthly(symbol, savingtoCsv=True):
    # gets data over of a week
    # loading necessary modules
    from alpha_vantage.timeseries import TimeSeries
    # getting api key
    API_KEY, waiting_times = api_key_finder()
    # creating object
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    # reading data into pandas
    data, meta_data = ts.get_monthly(symbol=symbol)
    # writing data to database and csv
    write_to_database(data, 'Monthly', symbol, 'monthly', savingtoCsv)
    return data, meta_data


def get_data_latest(symbol, savingtoCsv=True):
    # reads the latest data of the API
    # get changes of the last day
    from alpha_vantage.timeseries import TimeSeries
    API_KEY, waiting_times = api_key_finder()
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    data = ts.get_quote_endpoint(symbol=symbol)
    return data  # , waiting_times


if __name__ == "__main__":
    data, meta_data = get_data_intraday('AAPL', '5min', 'compact', True)
    d, m = get_data_weekly('IBM')
    # print(data.head())
    # print(meta_data)
