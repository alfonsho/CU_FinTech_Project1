import pandas as pd
import numpy as np
import os 
import requests
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi



class Doggie:
    def __init__(self, api="alpaca"):

        self.api = api
        if self.api == "alpaca":
            load_dotenv()
            self.alpaca_api_key = os.getenv("ALPACA_API_KEY")
            self.alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
            self.alpaca = tradeapi.REST(self.alpaca_api_key,
                                        self.alpaca_secret_key,
                                        api_version="V2")


    def fetch(self, tickers, timeframe, start, end):
        if self.api == "alpaca":

            t_0 = pd.Timestamp(start, tz="America/New_York").isoformat()
            t = pd.Timestamp(end, tz="America/New_York").isoformat()

            df_portfolio = self.alpaca.get_bars(
                tickers, 
                timeframe,
                t_0,
                t
            ).df

            return df_portfolio

        



    

    def __doc__(cls):
        return """This is a wrapper for various APIS. Currently just ALPACA"""


if __name__ == "__main__":
    lassie = Doggie()

    t_0 = "2020-07-14"
    t = "2022-5-9"
    tickers = ["FB", "TWTR", "AAPL","GOOG"]
    timeframe = "1D"

    bone = lassie.fetch(
            tickers,
            timeframe,
            start = t_0,
            end = t
    )

    print(bone)