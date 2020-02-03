#This program will test if the realtime data works
#Moreover it will test if the latest data works as well

import GetStockDate
from time import gmtime, strftime,sleep

symbol='AAPL'
interval='1min'
outputsize='compact'

while True:
    time=strftime("%Y-%m-%d %A %H:%M:%S", gmtime())
    time_day=strftime("%A", gmtime())
    time_hour=strftime("%H", gmtime())
    f = open("log.txt", "a")
    if time_day!="Sunday" and time_day!="Saturday" and int(time_hour)-4>8 and int(time_hour)-4<17:
        d,m=GetStockDate.get_data_intraday(symbol,interval,outputsize)
        print(GetStockDate.get_data_latest(symbol)['05. price']+'------------'+d.head(1))
        f.write(GetStockDate.get_data_latest(symbol)['05. price']+'------------'+d.head(1))
    else:
        f.write(time+'\n'+time_day+time_hour)
    f.close()
    sleep((7*60*60)/500)