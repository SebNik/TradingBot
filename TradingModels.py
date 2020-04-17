# this file is going to be filled with models which can trade out stock data
# loading class for link
from TradeStocks import Stock


class Model(Stock):

    def __init__(self, symbol, simulation=True, start_acc=10000, fee=0.01, interval='daily'):
        super().__init__(symbol, start_acc=start_acc, fee=fee, check_if_exists=False)
        self.sim = simulation
        self.interval = interval

    def __simple_high_low(self, open=0, close=0, high=0, low=0, volume=0):
        range_high = 0.9
        range_low = 1.1
        if open < close and high * range_high < close:
            units = self.get_possible_buy(price=close, fraction=0.5)
            self.buy(units, price=close)
        elif open < close:
            units = self.get_possible_buy(price=close, fraction=0.2)
            self.buy(units, price=close)
        elif open > close and low * range_low > close:
            abs, units = self.get_possible_sell(price=close, fraction=0.5)
            self.sell(units, price=close)
        elif open > close:
            abs, units = self.get_possible_sell(price=close, fraction=0.2)
            self.sell(units, price=close)

    def run(self):
        # this function will run all coded models
        if self.sim:
            # the simulation mode is on and the simulation is getting called
            # loading in simulation
            from SimulationStocks import Simulation
            # object sim is being created
            sim = Simulation(self.symbol, interval=self.interval, date_range=[[2004, 1, 1], [2004, 12, 31]])
            # data is loaded in for the for loop
            row, count, index = sim.get_price()
            # for loop with real stuff is starting
            for i in range(0, int(count['date'])):
                # reading new data from simulation
                row, count, index = sim.get_price(index=i)
                # setting vars for model
                close = float(row['4. close'])
                open = float(row['1. open'])
                high = float(row['2. high'])
                low = float(row['3. low'])
                volume = float(row['5. volume'])
                # calling model
                self.__simple_high_low(open=open, close=close, high=high, low=low, volume=volume)



    def analysis_numbers(self):
        # this function is calculating relevant numbers for a analysis
        profit =

if __name__ == '__main__':
    simple_model = Model('IBM')
    simple_model.run()
