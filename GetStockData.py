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


def clean_df_db_dups(df, tablename, engine, dup_cols=[],
                     filter_continuous_col=None, filter_categorical_col=None):
    import pandas as pd
    """
    Remove rows from a dataframe that already exist in a database
    Required:
        df : dataframe to remove duplicate rows from
        engine: SQLAlchemy engine object
        tablename: tablename to check duplicates in
        dup_cols: list or tuple of column names to check for duplicate row values
    Optional:
        filter_continuous_col: the name of the continuous data column for BETWEEEN min/max filter
                               can be either a datetime, int, or float data type
                               useful for restricting the database table size to check
        filter_categorical_col : the name of the categorical data column for Where = value check
                                 Creates an "IN ()" check on the unique values in this column
    Returns
        Unique list of values from dataframe compared to database table
    """
    args = 'SELECT %s FROM %s' % (', '.join(['"{0}"'.format(col) for col in dup_cols]), tablename)
    args_contin_filter, args_cat_filter = None, None
    if filter_continuous_col is not None:
        if df[filter_continuous_col].dtype == 'datetime64[ns]':
            args_contin_filter = """ "%s" BETWEEN Convert(datetime, '%s')
                                          AND Convert(datetime, '%s')""" % (filter_continuous_col,
                                                                            df[filter_continuous_col].min(),
                                                                            df[filter_continuous_col].max())

    if filter_categorical_col is not None:
        args_cat_filter = ' "%s" in(%s)' % (filter_categorical_col,
                                            ', '.join(["'{0}'".format(value) for value in
                                                       df[filter_categorical_col].unique()]))

    if args_contin_filter and args_cat_filter:
        args += ' Where ' + args_contin_filter + ' AND' + args_cat_filter
    elif args_contin_filter:
        args += ' Where ' + args_contin_filter
    elif args_cat_filter:
        args += ' Where ' + args_cat_filter
    df.drop_duplicates(dup_cols, keep='last', inplace=True)
    df = pd.merge(df, pd.read_sql(args, engine), how='left', on=dup_cols, indicator=True)
    df = df[df['_merge'] == 'left_only']
    df.drop(['_merge'], axis=1, inplace=True)
    return df


def get_data_intraday(symbol, interval, outputsize, savingtoCsv=False):
    # gets data over a period of a day
    # loading necessary modules
    from alpha_vantage.timeseries import TimeSeries
    from time import gmtime, strftime
    import sqlite3
    import os
    # getting the right api key
    API_KEY, waiting_times = api_key_finder()
    # setting the reading data
    ts = TimeSeries(key=API_KEY, output_format='pandas', indexing_type='integer')
    # reading the right time
    time = strftime("%Y-%m-%d-%A", gmtime())
    # getting the final data
    data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
    data.rename(columns={'index': 'date'}, inplace=True)
    # check if need to save to CSV-File
    if savingtoCsv:
        # saved data csv-file data
        data.to_csv(
            '/home/niklas/Desktop/TradingBot/StockData/' + 'StockData-' + symbol + '-' + interval + '-' + time + '.csv',
            sep=';')
    # time for loading the database
    file = '/home/niklas/Desktop/TradingBot/StockData/StockData-{}.db'.format(symbol)
    tablename = 'IntraDay' + symbol + interval
    if not os.path.isfile(file):
        conn = sqlite3.connect(file)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE {} (date1 TEXT, open2 REAL, high3 REAL, low4 REAL, close5 REAL, volume REAL)'.format(
                tablename))
    else:
        conn = sqlite3.connect(file)
        c = conn.cursor()
    # now the database is connected through
    # next we are going to check if the table already exists
    table_check = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(tablename)
    c.execute(table_check)
    result = c.fetchone()
    if result:
        # table found
        None
    else:
        # table not found
        c.execute(
            'CREATE TABLE {} (date1 TEXT, open2 REAL, high3 REAL, low4 REAL, close5 REAL, volume REAL)'.format(
                tablename))

    # -----------------------------------------------------------------------------------------------------------------
    # Working on
    # -----------------------------------------------------------------------------------------------------------------
    data.index.name = ' '
    #print(data.tail())
    import pandas as pd
    df = pd.read_sql_query("SELECT * FROM {}".format(tablename), conn)#, index_col='date')
    print(df.head())
    new_df = pd.concat([data,df], ignore_index=True)
    #print(new_df.tail())
    new_df.drop_duplicates(subset='date', keep='last', inplace=True, ignore_index=True)
    new_df.sort_values('date' ,inplace=True)
    new_df.to_csv('/home/niklas/Desktop/TradingBot/StockData/test.csv')

    #print(new_df.head())
    #print(new_df.tail())
    new_df.to_sql(tablename, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    # -----------------------------------------------------------------------------------------------------------------
    # End
    # -----------------------------------------------------------------------------------------------------------------

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
    data, meta_data = get_data_intraday('TSLA', '1min', 'compact')
    # print(data.head())
