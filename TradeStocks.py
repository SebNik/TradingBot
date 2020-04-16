# this file is responsible for all buying and selling actions and their logging
# the stock data is read out of the sqlite3 database


class Stock:
    def __init__(self, symbol, start_acc=1000, fee=0.01):
        self.symbol=symbol
        self.account=start_acc
        self.table_name=symbol.upper()+'-Account'
        self.broker_fee=fee


if __name__ == "__main__":
    None

