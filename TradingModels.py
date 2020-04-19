# this file is going to be filled with models which can trade out stock data
# loading class for link
from SimulationStocks import Simulation


class Model(Simulation):

    def __init__(self, symbol, simulation=True, start_acc=10000, fee=0.01, interval='daily', date_range=None):
        # sim object is being created
        super().__init__(symbol=symbol, interval=interval, date_range=date_range, start_acc=start_acc, fee=fee)
        self.sim = simulation
        if self.sim:
            row, count, index = self.get_price()
            self.sim_index = index
            self.sim_count = count

    def run(self):
        # this function will run all coded models
        if self.sim:
            # the simulation mode is on and the simulation is getting called
            # for loop with real stuff is starting
            for i in range(0, int(self.sim_count['date'])):
                # reading new data from simulation
                row, count, index = self.get_price(index=i)
                # setting vars for model
                close = float(row['4. close'])
                open = float(row['1. open'])
                high = float(row['2. high'])
                low = float(row['3. low'])
                volume = float(row['5. volume'])
                date = row['date']
                # setting last nums
                self.sim_close = close
                # calling model
                self.__simple_high_low(open=open, close=close, high=high, low=low, volume=volume, date_sim=date)

    def __simple_high_low(self, open=0, close=0, high=0, low=0, volume=0, date_sim=0):
        range_high = 0.9
        range_low = 1.1
        if open < close and high * range_high < close:
            units = self.get_possible_buy(price=close, fraction=0.5)
            self.buy(units, price=close, date_sim=date_sim)
        elif open < close:
            units = self.get_possible_buy(price=close, fraction=0.2)
            self.buy(units, price=close, date_sim=date_sim)
        elif open > close and low * range_low > close:
            abs, units = self.get_possible_sell(price=close, fraction=0.5)
            self.sell(units, price=close, date_sim=date_sim)
        elif open > close:
            abs, units = self.get_possible_sell(price=close, fraction=0.2)
            self.sell(units, price=close, date_sim=date_sim)

    def _get_depot_value(self):
        last_price = self.sim_close
        return float(self.account + (self.units * last_price))

    def _get_profit(self):
        return float(self._get_depot_value() / self.start_acc)

    def analysis_numbers(self, to_json_file=False):
        # this function is calculating relevant numbers for a analysis
        # loading modules to json export
        import json
        # getting values for analysis
        profit = self._get_profit()
        buys, sells = self.get_transaction_count()
        depot_value = self._get_depot_value()
        # creating dictonary for export
        dic = {
            'Depot': depot_value,
            'Profit': profit,
            'Buys': buys,
            'Sells': sells
        }
        # checking if needed to export to json file
        if to_json_file:
            # creating file
            with open('/home/niklas/Desktop/TradingBot/Analysis/analysis-model-numbers.json', 'w') as fp:
                json.dump(dic, fp)
        # retuning dic
        return dic

    def analysis_transaction_time_graph(self):
        # this function will plot a graph which shows the buy and sell times
        # loading modules
        import json
        import datetime
        import matplotlib.pyplot as plt
        # reading in json parameters
        with open('/home/niklas/Desktop/TradingBot/Parameters/graph.json') as json_file:
            parameters = json.load(json_file)
        # changing index of stock data to date for x axis
        self.data.set_index('date', inplace=True)
        # reading in the transactions data
        df_transactions = self.get_transaction_df()
        df_transactions['Time'] = df_transactions['Time'].apply(lambda x: datetime.datetime.utcfromtimestamp(float(x)).strftime('%Y-%m-%d'))

        buy_transactions = df_transactions[df_transactions['ID_Function'] == 'S-BUY']
        sell_transactions = df_transactions[df_transactions['ID_Function'] == 'S-SELL']


        #df_transactions.set_index('Time', inplace=True)
        #buy_transactions.set_index('Time', inplace=True)
        # filtering the data with buy and sell

        print(buy_transactions.head(15))
        # creating figure in which deploy
        fig=plt.figure(figsize=(parameters['screen_x'], parameters['screen_y']), dpi=parameters['dpi'])
        ax = fig.add_subplot(111)
        # setting style
        #plt.style.use('seaborn-darkgrid')
        # define title of plot
        plt.title(**parameters['title'])
        # setting x-axis and y-axis
        plt.ylabel(parameters['y_label']['label'], parameters['y_label'])
        plt.xlabel(parameters['x_label']['label'], parameters['x_label'])
        # grid settings
        #plt.grid(b=True, **parameters['grid'])
        # starting plotting price line
        #self.data['4. close'].plot(**parameters['line1'])
        #df_transactions['price_each'].plot(**parameters['line1'])
        #buy_transactions['price_each'].plot()
        plt.plot(df_transactions['Time'], df_transactions['price_each'], **parameters['line1'])
        plt.scatter(buy_transactions['Time'], buy_transactions['price_each'])
        import numpy as np
        plt.xticks(np.arange(len(self.dates_list)),self.dates_list,rotation=30)
        spacing=2
        for label in ax.xaxis.get_ticklabels()[::spacing]:
            label.set_visible(False)

        #plt.set_xticks(np.arange(len(short_dates)))
        #ax.set_xticklabels(short_dates)
        # showing the legend
        plt.legend(**parameters['legend'])
        # showing the final graph
        plt.show()


if __name__ == '__main__':
    simple_model = Model('IBM', date_range=[[2004, 1, 1], [2004, 2, 20]])
    simple_model.run()
    analysis_numbers_dict = simple_model.analysis_numbers(to_json_file=True)
    print(analysis_numbers_dict)
    simple_model.analysis_transaction_time_graph()
