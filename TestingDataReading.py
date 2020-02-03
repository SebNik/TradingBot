#This program will test if the realtime data works
#Moreover it will test if the latest data works as well

import GetStockDate
from time import gmtime, strftime,sleep
import pandas as pd

symbol='AAPL'
interval='1min'
outputsize='compact'

while True:
    time=strftime("%Y-%m-%d %A %H:%M:%S", gmtime())
    time_day=strftime("%A", gmtime())
    time_hour=strftime("%H", gmtime())
    f = open("log.txt", "a")
    if time_day!="Sunday" and time_day!="Saturday" and int(time_hour)-5>7 and int(time_hour)-5<17:
        d,m=GetStockDate.get_data_intraday(symbol,interval,outputsize)
        latest_data=GetStockDate.get_data_latest(symbol)['05. price']
        #print(latest_data+'------------'+d.head(1))
        f.write(latest_data.to_string(index=False)+'------------'+d.head(1)['4. close'].to_string(index=False)+'\n'+'-------------'+'\n')
    else:
        f.write(time+time_day+time_hour+'\n')
    f.close()
    sleep((7*60*60)/500)