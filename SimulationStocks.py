# this file is responsible to manipulate stock prices in any given way
# the easiest option would be to to this with historical dat
from TradeStocks import Stock


class Simulation(Stock):
    def __init__(self, symbol, interval='daily', date_range=None, start_acc=1000, fee=0.01):
        # loading in modules
        import GetStockData
        import sqlite3
        import pandas as pd
        import datetime
        # setting Stock data class
        super().__init__(symbol=symbol, start_acc=start_acc, fee=fee)
        # setting self.vars
        self.symbol = symbol
        self.interval = interval
        self.file = '/home/niklas/Desktop/TradingBot/StockData/StockData-{}.db'.format(symbol)
        # starting checking for right playing option
        if self.interval == 'daily':
            GetStockData.get_data_daily(self.symbol, 'full', savingtoCsv=True)
            self.table_name = 'Daily' + self.symbol + 'daily'
        if self.interval == 'weekly':
            GetStockData.get_data_weekly(self.symbol, savingtoCsv=False)
            self.table_name = 'Weekly' + self.symbol + 'weekly'
        if self.interval == 'monthly':
            GetStockData.get_data_monthly(self.symbol, False)
            self.table_name = 'Monthly' + self.symbol + 'monthly'
        if self.interval == 'intraday':
            GetStockData.get_data_intraday(symbol, '1min', 'full', savingtoCsv=False)
            self.table_name = 'IntraDay' + self.symbol + 'min'
        # getting pandas document
        # connecting to database
        conn = sqlite3.connect(self.file)
        # reading the database into  pandas dataframe
        df = pd.read_sql_query("SELECT * FROM {}".format(self.table_name), conn)
        # reversing the dataframe
        df = df.iloc[::-1]
        # filtering data
        if date_range is not None:
            # setting vars
            self.date1 = datetime.datetime(date_range[0][0], date_range[0][1], date_range[0][2]).timestamp()
            self.date2 = datetime.datetime(date_range[1][0], date_range[1][1], date_range[1][2]).timestamp()
            self.date_range = date_range
            # creating list with dates with pandas nly buisness days included
            dates_list = pd.bdate_range(datetime.datetime.utcfromtimestamp(self.date1).strftime('%Y-%m-%d %H:%M:%S'),
                                        datetime.datetime.utcfromtimestamp(self.date2).strftime('%Y-%m-%d %H:%M:%S')
                                        ).strftime("%Y-%m-%d").tolist()
            df_filtered = df[df['date'].isin(dates_list)]
            self.data = df_filtered
            self.data.reset_index(inplace=True, drop=True)
        else:
            self.data = df
            self.date1 = 0
            self.date2 = 0
            self.date_range = date_range
        # counting rows in dataframe
        self.row_count = self.data.count()

    def get_price(self, index=0):
        row_data = self.data.loc[index, :]
        return row_data, self.row_count, index

    def __str__(self):
        return 'Simulation: Symbol: ' + self.symbol + ' Interval: ' + self.interval


if __name__ == "__main__":
    sim = Simulation('IBM', interval='daily', date_range=[[2004, 1, 1], [2004, 12, 31]])
    d, c, i = sim.get_price()
    print(d)
