#all data is from GMT-5 -> Time Germany -6

def api_key_finder():
    #selctes the right api key for maximal sucees
    from time import gmtime, strftime
    import os
    #500 requests a day -- 5 per min
    file_api='api-key_logs.txt'
    api_keys=['U5C8JI4ELG45JNT7','L7C6HSQARL8LR5E4','D7TUJ5FRXFV44XPO','2EGXAE0H594DZ9U5']
    selected_api_key=''
    #log format:%Y+%m+%d-%A+%H:%M:%S-APIKEYNO-APIKEY-requests
    trading_hours=6.5
    resolution_data=((trading_hours*60*60)/500)/len(api_keys)
    #gives how many seconds are between possible requests
    calls_per_key_per_min=60/resolution_data*len(api_keys)
    if calls_per_key_per_min<6:
        #not possible
        while calls_per_key_per_min<6:
            calls_per_key_per_min=60/resolution_data*len(api_keys)
            resolution_data+=0.25
    #ideal call time is resoulution_data
    if (os.path.isfile(file_api)==False):
        f=open(file_api, 'x')
        f.write('-Logs of APIs-\n')
        f.close()
    f=open(file_api, 'r')
    api_key_logs=f.readlines()
    last_api_key_log=api_key_logs[-1].split('-')
    f.close()
    time=strftime("%Y+%m+%d-%A+%H:%M:%S", gmtime())
    time_day=strftime("%Y+%m+%d", gmtime())
    #opens for logging
    f=open(file_api, 'a')
    #starting to check
    if (last_api_key_log[0]==time_day):
        if (api_keys[int(last_api_key_log[2])]==last_api_key_log[3]):
            selected_api_key=api_keys[int(last_api_key_log[2])+1]
            f.write(time+'-'+str(int(last_api_key_log[2])+1)+'-'+selected_api_key+'-'+str(int(last_api_key_log[4])+1)+'\n')
    else:
        from random import randint
        no=randint(0,len(api_keys)-1)
        selected_api_key=api_keys[no]
        f.write(time+'-'+str(no)+'-'+selected_api_key+'-'+'0'+'\n')
    f.close()
    #closing and saving file


def get_data_intraday(symbol,interval,outputsize,savingtoCsv=True):
    #gets data over a periode of a day
    from alpha_vantage.timeseries import TimeSeries

    ts = TimeSeries(key=API_KEY,output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol,interval=interval, outputsize=outputsize)
    if savingtoCsv:
        data.to_csv('/home/niklas/Desktop/TradingBot/StockData/' + 'StockData-' + symbol + '-' + interval +'.csv',sep=';')
    return data,meta_data

def get_data_latest(symbol,savingtoCsv=False):
    #reads the latest data of the API
    #get changes of the last day
    from alpha_vantage.timeseries import TimeSeries

    ts = TimeSeries(key=API_KEY,output_format='pandas')
    data = ts.get_quote_endpoint(symbol=symbol)
    return data[0]

if __name__ == "__main__":
    API_KEY = 'U5C8JI4ELG45JNT7'
    API_KEY_2='L7C6HSQARL8LR5E4'
    API_KEY_3='D7TUJ5FRXFV44XPO'
    API_KEY_4='2EGXAE0H594DZ9U5'
    symbol='MSFT'
    interval='1min'
    outputsize='compact'
    #data,meta_data=get_data_intraday(API_KEY,symbol,interval,outputsize)
    #print(meta_data)
    #print(data.head(1))
    #print(get_data_latest(API_KEY,symbol)['05. price'])
    print(api_key_finder())
    print(api_key_finder())
    print(api_key_finder())
    print(api_key_finder())
    print(api_key_finder())
    print(api_key_finder())
    print(api_key_finder())
    print(api_key_finder())