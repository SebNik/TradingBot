# this file is responsible for all buying and selling actions and their logging
# the stock data is read out of the sqlite3 database


class Stock:
    def __init__(self, symbol, start_acc=1000, fee=0.01):
        self.symbol = symbol
        self.account = start_acc
        self.table_name = symbol.upper() + '-Account'
        self.broker_fee = fee
        self.units = 0

    def log_to_database(self):
        # this function will write the log for transactions
        # loading the needed modules
        import os
        import sqlite3
        import pandas as pd
        # checking for database
        # time for loading the database
        file = '/home/niklas/Desktop/TradingBot/StockData/StockData-{}.db'.format(symbol)
        tablename = name + symbol + interval
        if not os.path.isfile(file):
            conn = sqlite3.connect(file)
            c = conn.cursor()
            c.execute(
                'CREATE TABLE {} (date1 TEXT, open2 REAL, high3 REAL, low4 REAL, close5 REAL, volume REAL)'.format(
                    tablename))
        else:
            conn = sqlite3.connect(file)
            c = conn.cursor()
            # now the database is connected through
            # next we are going to check if the table already exists
            table_check = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(tablename)
            c.execute(table_check)
            result = c.fetchone()
            if result:
                # table found
                None
            else:
                # table not found
                c.execute(
                    'CREATE TABLE {} (date1 TEXT, open2 REAL, high3 REAL, low4 REAL, close5 REAL, volume REAL)'.format(
                        tablename))
            # read data which is already in database
            df = pd.read_sql_query("SELECT * FROM {}".format(tablename), conn)  # , index_col='date')
            # dataframes joined after each other
            new_df = pd.concat([data, df], ignore_index=True)
            # duplicates are removed
            new_df.drop_duplicates(subset='date', keep='last', inplace=True, ignore_index=True)
            # sorting dataframe by values
            new_df.sort_values('date', inplace=True, ascending=False)
            # check if need to save to CSV-File
            if savingtoCsv:
                # saved data csv-file data
                new_df.to_csv(
                    '/home/niklas/Desktop/TradingBot/StockData/' + 'StockData-' + symbol + '-' + interval + '.csv',
                    sep=';')
            # write data to database
            new_df.to_sql(tablename, conn, if_exists='replace', index=False)
            conn.commit()
            conn.close()

    def read_stock_price(self):
        import GetStockData
        data_latest = GetStockData.get_data_latest(self.symbol)
        return data_latest

    def change(self, value):
        self.account += value
        self.log_to_database()

    def buy(self, units_to_buy):
        latest = self.read_stock_price()
        last_price = latest[0]['05. price'][0]
        self.units += units_to_buy
        self.account -= units_to_buy * float(last_price) + units_to_buy * self.broker_fee
        self.log_to_database()

    def sell(self, units_to_sell):
        None

    @classmethod
    def classmethod(cls):
        return 'class method called', cls

    def __repr__(self):
        return self

    def __str__(self):
        return 'Symbol: ' + self.symbol + ' Balance: ' + str(self.account) + ' Units: ' + str(self.units)


if __name__ == "__main__":
    ibm = Stock('IBM')
    print(ibm.account)
    ibm.buy(4)
    print(ibm.account)
    print(ibm)
