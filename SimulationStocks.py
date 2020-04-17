# this file is responsible to manipulate stock prices in any given way
# the easiest option would be to to this with historical dat


class Simulation:
    def __init__(self, symbol, interval='daily'):
        # loading in modules
        import GetStockData
        # setting self.vars
        self.symbol = symbol
        self.interval = interval
        self.file = '/home/niklas/Desktop/TradingBot/StockData/StockData-{}.db'.format(symbol)
        # starting checking for right playing option
        if self.interval == 'daily':
            a,b=GetStockData.get_data_daily(self.symbol, 'full', savingtoCsv=False)
            self.table_name = 'Daily' + self.symbol + 'daily'
        if self.interval == 'weekly':
            GetStockData.get_data_weekly(self.symbol,savingtoCsv=False)
            self.table_name = 'Weekly' + self.symbol + 'weekly'
        if self.interval == 'monthly':
            GetStockData.get_data_monthly(self.symbol, False)
            self.table_name = 'Monthly' + self.symbol + 'monthly'
        if self.interval == 'intraday':
            GetStockData.get_data_intraday(symbol, '1min', 'full', savingtoCsv=False)
            self.table_name = 'IntraDay' + self.symbol + 'min'

    def get_price(self, index=0):
        # importing modules
        import sqlite3
        import pandas as pd
        # connecting to database
        conn = sqlite3.connect(self.file)
        # reading the database into  pandas dataframe
        df = pd.read_sql_query("SELECT * FROM {}".format(self.table_name), conn)
        row_data = df.loc[index, :]
        row_count=df.count()
        return row_data, row_count, index

    def __str__(self):
        return 'Simulation: Symbol: ' + self.symbol + ' Interval: ' + self.interval


if __name__ == "__main__":
    sim = Simulation('IBM', interval='daily')
    d,c,i=sim.get_price()
    print(d)
