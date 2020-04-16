# this file is responsible for all buying and selling actions and their logging
# the stock data is read out of the sqlite3 database


class Stock:
    def __init__(self, symbol, start_acc=1000, fee=0.01):
        self.symbol=symbol
        self.account=start_acc
        self.table_name=symbol.upper()+'-Account'
        self.broker_fee=fee
        self.units=0


    def log_to_database(self):
        None


    def read_stock_price(self):
        None


    def change(self, value):
        self.account+=value
        self.log_to_database()


    def buy(self,units_to_buy):
        None


    def sell(self, units_to_sell):
        None


if __name__ == "__main__":
    None

