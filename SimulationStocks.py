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
            GetStockData.get_data_daily(self.symbol, False)
            self.table_name = 'Daily' + self.symbol + 'daily'
        if self.interval=='weekly':
            GetStockData.get_data_weekly(self.symbol)
            self.table_name = 'Weekly' + self.symbol + 'weekly'
        if self.interval == 'monthly':
            GetStockData.get_data_monthly(self.symbol, False)
            self.table_name='Monthly'+self.symbol+'monthly'
        if self.interval == 'intrday':
            GetStockData.get_data_intraday(symbol, '1min', 'full', savingtoCsv=False)
            self.table_name = 'IntraDay' + self.symbol + 'min'

    def get_price(self):

        df = pd.read_sql_query("SELECT * FROM {}".format(tablename), conn)  # , index_col='date')

    def __str__(self):
        return 'Simulation: Symbol: ' + self.symbol + ' Interval: ' + self.interval


if __name__ == "__main__":
    sim = Simulation('IBM')
