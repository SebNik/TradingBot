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


if __name__ == '__main__':
    unittest.main()
