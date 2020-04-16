# this file is responsible to manipulate stock prices in any given way
# the easiest option would be to to this with historical dat


class Simulation:
    def __init__(self, symbol, interval='daily'):
        # loading in modules
        import GetStockData
        # setting self.vars
        self.symbol=symbol
        self.interval=interval
        # starting checking for right playing option
        if self.interval == 'daily':
            GetStockData.get_data_daily(self.symbol,False)
        if self.interval == 'monthly':
            GetStockData.get_data_monthly(self.symbol,False)
        if self.interval == 'intrday':
            GetStockData.get_data_intraday(symbol, '1min', 'full', savingtoCsv=False)


if __name__ == "__main__":
    sim = Simulation('IBM')
