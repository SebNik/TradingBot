# this file is responsible to manipulate stock prices in any given way
# the easiest option would be to to this with historical dat


class Simulation:
    def __init__(self, symbol, interval='daily'):
        import GetStockData
        if interval == 'daily':
            d, m = GetStockData.get_data_intraday(symbol, '1min', 'compact', savingtoCsv=True)
        if interval == 'monthly':
            None
        if interval == 'intrday':
            None


if __name__ == "__main__":
    sim = Simulation('IBM')
