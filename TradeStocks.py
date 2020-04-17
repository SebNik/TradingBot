# this file is responsible for all buying and selling actions and their logging
# the stock data is read out of the sqlite3 database


class Stock:
    def __init__(self, symbol, start_acc=1000, fee=0.01, check_if_exists=False):
        # this function is the init
        self.symbol = symbol
        self.table_name = symbol.upper() + '_Account'
        # checking if possible to read from older version
        if check_if_exists:
            # this function will check if there is old data that can be used
            # loading the needed modules
            import os
            import sqlite3
            import pandas as pd
            # creating path
            file = '/home/niklas/Desktop/TradingBot/Transactions/Transactions-{}.db'.format(self.symbol)
            # checking if database already exists
            if os.path.isfile(file):
                # already existing, establishing connection
                conn = sqlite3.connect(file)
                c = conn.cursor()
                # now the database is connected through
                # next we are going to check if the table already exists
                table_check = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(self.table_name)
                c.execute(table_check)
                result = c.fetchone()
                if result:
                    # table found
                    # read data which is already in database
                    df = pd.read_sql_query("SELECT * FROM {}".format(self.table_name), conn)
                    # setting vars
                    self.account = float(df.tail(1)['account'])
                    self.broker_fee = float(df.tail(1)['fee'])
                    self.units = int(df.tail(1)['units'])
            else:
                self.account = start_acc
                self.broker_fee = fee
                self.units = 0
        else:
            self.account = start_acc
            self.broker_fee = fee
            self.units = 0

    def _log_to_database(self, action, last_price=0, units=0, savingtoCsv=True):
        # this function will write the log for transactions
        # loading the needed modules
        import os
        import sqlite3
        import pandas as pd
        from datetime import datetime
        # checking for database
        # creating path
        file = '/home/niklas/Desktop/TradingBot/Transactions/Transactions-{}.db'.format(self.symbol)
        # getting current time
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        # checking if already exists
        if not os.path.isfile(file):
            # creating file and table
            conn = sqlite3.connect(file)
            c = conn.cursor()
            c.execute(
                'CREATE TABLE {} (Time TEXT, ID_Function TEXT, ID TEXT, symbol TEXT, price_each REAL, units REAL, '
                'price_total REAL, profit REAL, fee REAL, account REAL)'.format(self.table_name))
        else:
            # already existing, establishing connection
            conn = sqlite3.connect(file)
            c = conn.cursor()
            # now the database is connected through
            # next we are going to check if the table already exists
            table_check = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(self.table_name)
            c.execute(table_check)
            result = c.fetchone()
            if result:
                # table found
                None
            else:
                # table not found
                c.execute(
                    'CREATE TABLE {} (Time TEXT, ID_Function TEXT, ID TEXT, symbol TEXT, price_each REAL, units REAL, '
                    'price_total REAL, profit REAL, fee REAL, account REAL)'.format(self.table_name))
        # read data which is already in database
        df = pd.read_sql_query("SELECT * FROM {}".format(self.table_name), conn)
        # calculating profit
        if action == 'BUY':
            profit = -100 * float(self.account) / float(float(self.account) + float(units * float(last_price)))
        elif action == 'SELL':
            profit = 100 * float(self.account) / float(float(self.account) + float(units * float(last_price)))
        else:
            profit = 0
        # counting rows
        index = df.index
        count = len(index)
        # creating row with data
        # starting with dictionary
        row_dict = {
            'Time': [timestamp],
            'ID_Function': [action],
            'ID': [count],
            'symbol': [self.symbol],
            'price_each': [last_price],
            'units': [units],
            'price_total': [float(units * float(last_price))],
            'profit': [profit],
            'fee': [self.broker_fee],
            'account': [self.account]
        }
        df_row = pd.DataFrame(row_dict)
        # new row added to new dataframe
        new_df = pd.concat([df, df_row], ignore_index=True)
        # check if need to save to CSV-File
        if savingtoCsv:
            # saved data csv-file data
            new_df.to_csv('/home/niklas/Desktop/TradingBot/Transactions/Transactions-{}.csv'.format(self.symbol),
                          sep=';')
        # write data to database
        new_df.to_sql(self.table_name, conn, if_exists='replace', index=False)
        # committing the saves
        conn.commit()
        # closing the connection
        conn.close()

    def __read_stock_price(self):
        # read the stock price latest
        import GetStockData
        data_latest = GetStockData.get_data_latest(self.symbol)
        return data_latest

    def change(self, value):
        # manually recharging the account
        self.account += value
        self._log_to_database('CHANGE')

    def buy(self, units_to_buy, price=0):
        # buying stocks
        # check for simulation
        if price == 0:
            # no simulation uses real
            latest = self.__read_stock_price()
            last_price = latest[0]['05. price'][0]
            # use normal state
            state = 'BUY'
        else:
            # simulation use given price
            last_price = price
            # set different state
            state = 'S-BUY'
        self.units += units_to_buy
        self.account -= units_to_buy * (float(last_price) + units_to_buy * self.broker_fee)
        self._log_to_database(state, last_price=last_price, units=units_to_buy, savingtoCsv=True)

    def sell(self, units_to_sell, price=0):
        # selling stocks
        if self.units >= units_to_sell:
            if price == 0:
                # no simulation uses real
                latest = self.__read_stock_price()
                last_price = latest[0]['05. price'][0]
                # use normal state
                state = 'SELL'
            else:
                # simulation use given price
                last_price = price
                # set different state
                state = 'S-SELL'
            self.units -= units_to_sell
            self.account += units_to_sell * (float(last_price) - units_to_sell * self.broker_fee)
            self._log_to_database(state, last_price=last_price, units=units_to_sell, savingtoCsv=True)

    def get_last_log(self, lines=1):
        # loading the needed modules
        import sqlite3
        import pandas as pd
        # setting file path
        file = '/home/niklas/Desktop/TradingBot/Transactions/Transactions-{}.db'.format(self.symbol)
        # establishing connection to database
        conn = sqlite3.connect(file)
        # read data which is already in database
        df = pd.read_sql_query("SELECT * FROM {}".format(self.table_name), conn)
        # closing connection
        conn.close()
        # returning head(1)
        return df.tail(lines)

    def get_possible_buy(self, price=0, fraction=1):
        # this function will find out how many units can be bought
        if price == 0:
            # no simulation uses real
            latest = self.__read_stock_price()
            # reading price from dantaframe
            price = latest[0]['05. price'][0]
        # setting starting point
        units = 1
        # iterating and checking how much possible
        while self.account / (units * price) > 1:
            units += 1
        # callculating with fraction
        possible_buys = units * fraction
        # retuning value
        return possible_buys

    def get_possible_sell(self, price=0, fraction=1):
        # this function will find out how many units can be sold
        if price == 0:
            # no simulation uses real
            latest = self.__read_stock_price()
            # reading price from dantaframe
            price = latest[0]['05. price'][0]
        # checking how many sells
        possible_sells = self.units * fraction
        # calculating profits
        profit_abs = (possible_sells * self.broker_fee) * self.units
        # retuning vales
        return profit_abs, possible_sells

    def __repr__(self):
        return self

    def __str__(self):
        return 'Symbol: ' + self.symbol + ' Balance: ' + str(self.account) + ' Units: ' + str(
            self.units) + ' Tabel name: ' + self.table_name


if __name__ == "__main__":
    ibm = Stock('IBM', check_if_exists=True)
    ibm.buy(4, price=100)
    print(ibm.get_last_log())
    print(ibm.get_possible_buy(price=100))
