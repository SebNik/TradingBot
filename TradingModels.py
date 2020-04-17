# this file is going to be filled with models which can trade out stock data
# loading class for link
from TradeStocks import Stock


class Model(Stock):

    def __init__(self, symbol, simulation=True, start_acc=1000, fee=0.01, interval='daily'):
        super().__init__(symbol, start_acc=start_acc, fee=fee, check_if_exists=False)
        self.sim = simulation
        self.interval = interval


    def simple_high_low(self, open, close, high, low, volume):
        print('Moin')

    def run(self):
        # this function will run all coded models
        if self.sim:
            # the simulation mode is on and the simulation is getting called
            # loading in simulation
            from SimulationStocks import Simulation
            # object sim is being created
            sim = Simulation(self.symbol, interval=self.interval)
            # data is loaded in for the for loop
            row, count, index = sim.get_price()
            # for loop with real stuff is starting
            for i in range(0, int(count['date'])):
                row, count, index = sim.get_price(index=i)
                close = float(row['4. close'])
                open = float(row['1. open'])
                high = float(row['2. high'])
                low = float(row['3. low'])
                volume = float(row['5. volume'])


if __name__ == '__main__':
    simple_model = Model('IBM')
    simple_model.run()
