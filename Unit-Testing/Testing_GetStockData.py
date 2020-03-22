# This is a unit test for our stock data reading code
import unittest


class MyTestCase(unittest.TestCase):
    def test_api_key_finder(self):
        import GetStockData
        # we test if the right key is selected
        # first we check if the log file is existing
        import os
        file_api = 'api-key_logs.txt'
        self.assertTrue(os.path.isfile('/home/niklas/Desktop/TradingBot/' + file_api))
        # secondly we check if the resolution time is right
        from time import gmtime, strftime
        api_keys = 7
        closing_sec = 16 * 60 * 60
        trading_sec = closing_sec - (((int(strftime("%H", gmtime())) - 5) * 60) + int(strftime("%M", gmtime()))) * 60
        resolution_data_test = (trading_sec / 500) / api_keys
        selected_api_key, resolution_data = GetStockData.api_key_finder()
        self.assertEqual(resolution_data, str(resolution_data_test))
        # thirdly we check if the new api key is not the last one used
        selected_api_key_2, resolution_data = GetStockData.api_key_finder()
        self.assertNotEqual(selected_api_key, selected_api_key_2)

    def test_get_intraday(self):
        import GetStockData
        from time import gmtime, strftime, sleep
        import os
        import csv
        # this is going to test the intraday function
        # we can't actually check the data because it's changing every moment
        # firstly we are going to check if the excel table with the data exists
        # secondly we are going to check if the table in the excel is right
        # we will do this by calling all possible options
        # we try to pick long living stocks that will be there in a few months still
        symbols = ['AAPL']
        outputsizes = ['compact']
        intervalls = ['15min']
        saving_csv = [True]
        result = ['date', '1. open', '2. high', '3. low', '4. close', '5. volume']
        for sy in symbols:
            for csv_status in saving_csv:
                for out in outputsizes:
                    for inter in intervalls:
                        time = strftime("%Y-%m-%d-%A", gmtime())
                        file_path = '/home/niklas/Desktop/TradingBot/StockData/' + 'StockData-' + sy + '-' + inter + '-' + time + '.csv'
                        data, meta_data = GetStockData.get_data_intraday(sy, inter, out, csv_status)
                        self.assertTrue(os.path.isfile(file_path))
                        with open(file_path) as csv_file:
                            csv_reader = csv.reader(csv_file, delimiter=';')
                            for row in csv_reader:
                                self.assertEqual(row, result)
                                break
                        sleep(60 / 5 + 1)


if __name__ == '__main__':
    unittest.main()
