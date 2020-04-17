# this file is going to be filled with models which can trade out stock data
# loading class for link
from TradeStocks import Stock


class Model(Stock):
    def __init__(self, symbol, simulation=True, start_acc=1000, fee=0.01):
        super().__init__(symbol, start_acc=start_acc, fee=fee, check_if_exists=False)
        self.sim = simulation

    def run(self):
        # this function will run all coded models
        if self.sim:
            from SimulationStocks import Simulation
            sim = Simulation(self.symbol)
            row, count, index = sim.get_price()
            for i in range(0, int(count['date'])):
                print(float(row['4. close']))


if __name__ == '__main__':
    simple_model = Model('IBM')
    simple_model.run()
