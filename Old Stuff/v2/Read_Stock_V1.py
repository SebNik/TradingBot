def sim():
        import random
        return random.randint(0,1000)

def read_share_live(share_symbol,delay):
        import time
        lt=time.localtime()
        time_real=time.strftime('%d.%m.%Y;%H.%M.%S',lt)
        x=time_real
        from iexfinance.stocks import Stock
        share=Stock(share_symbol)
        price=share.get_price()
        y=price
        time.sleep(delay)
        return x,y

def get_stock_data(symbol,status,outputsize,interval='',date=''):
        import requests
        API_KEY = 'U5C8JI4ELG45JNT7'
        r = requests.get('https://www.alphavantage.co/query?function=' + status + '&symbol=' + symbol + '&interval=' + interval + 'min&outputsize=' + outputsize + '&apikey=' + API_KEY)
        if (r.status_code == 200):
                print('All clear')
        result = r.json()
        #print(result)
        if interval!='':
                dataForAllDays = result['Time Series (' + interval + 'min)']
                #print(dataForAllDays)
        else:
                dataForAllDays = result['Time Series (Daily)']
        #print(dataForAllDays)
        dataForSingleDate = dataForAllDays[date]
        print(dataForSingleDate['1. open'])
        print(dataForSingleDate['2. high'])
        print(dataForSingleDate['3. low'])
        print(dataForSingleDate['4. close'])
        print(dataForSingleDate['5. volume'])

import time
lt=time.localtime()
time_real=time.strftime('%Y-%m-%d %H:%M:00',lt)
print(time_real,int(time_real[14:16])-2)
time_new_york=time_real[0:11]+str(int(time_real[11:13])-6)+':'+str(int(time_real[14:16])-1)+':00'
print(time_new_york)
get_stock_data('AAPL','TIME_SERIES_INTRADAY', 'compact','1',time_new_york)
#TIME_SERIES_INTRADAY
#TIME_SERIES_DAILY
#compact last 100 full all data
#https://www.alphavantage.co/documentation/#intraday