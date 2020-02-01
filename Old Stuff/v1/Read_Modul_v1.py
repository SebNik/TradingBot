#Das Modul kann einen Aktienkurs slesen
#Dies geschiet Live
#Der Name der Aktie muss als Kürzel angegeben werdenn

def read_share_live(share_symbol,delay):
    try:
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
    except:
        return 'error3'

def read_share_history(share_symbol,start,end):
    try:
        from datetime import datetime
        from iexfinance.stocks import get_historical_data
        #Beispiel für Datum: 30.01.2000
        #--------------------0123456789
        start_time=datetime(int(start[6:]),int(start[3:5]),int(start[0:2]))
        end_time=datetime(int(end[6:]),int(end[3:5]),int(end[0:2]))
        data=get_historical_data(share_symbol, start_time, end_time)
        return data
    except:
        return 'error3'

def read_shares_minutly(share_symbol,date):
    try:
        from datetime import datetime
        from iexfinance.stocks import get_historical_intraday
        date_time = datetime(int(date[6:]),int(date[3:5]),int(date[0:2]))
        data=get_historical_intraday(share_symbol, date_time)
        return data
    except:
        return 'error3'