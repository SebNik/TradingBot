#This program will test if the realtime data works
#Moreover it will test if the latest data works as well

import GetStockDate
import time
from time import gmtime, strftime

API_KEY = 'U5C8JI4ELG45JNT7'
symbol='MSFT'
interval='1min'
outputsize='compact'

while True:
    time=strftime("%Y-%m-%d %A %H:%M:%S", gmtime())
    time_day=strftime("%A", gmtime())
    time_hour=strftime("%H", gmtime())
    #print(time)
    if time_day!="Sunday" and time_day!="Saturday" and int(time_hour)-4>8 and int(time_hour)-4<17:
        d,m=GetStockDate.get_data_intraday(API_KEY,symbol,interval,outputsize)
        print(GetStockDate.get_data_latest(API_KEY,symbol)['05. price']+'------------'+d.head(1))
        time.sleep(7*60*60/500)