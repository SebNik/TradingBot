import io
import requests
import pandas as pd


base = "https://api.iextrading.com/1.0/"

def get_last_price(symbol):
    payload = {
        "format": "csv",
        "symbols": symbol
    }
    endpoint = "tops/last"

    raw = requests.get(base + endpoint, params=payload)
    raw = io.BytesIO(raw.content)
    print(raw)
    prices_df = pd.read_csv(raw, sep=",")
    print(prices_df)
    prices_df["time"] = pd.to_datetime(prices_df["time"], unit="ms")
    prices_df["display_time"] = prices_df["time"].dt.strftime("%m-%d-%Y %H:%M:%S.%f")

    #print(prices_df)
    #print(prices_df.all())
    #print(prices_df['date'])    

while True:
    get_last_price('ADS')
