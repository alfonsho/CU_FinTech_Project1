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
        """
        This is a wrapper for the ALPACA api. 

        INPUTS:
        ------
            tickers: a list of strings, representing tickers. 
            timeframe: one of the following:
                                "1D", 
            start: the start date as a string. Ex. 2020-5-9
            end:   the end date. see start for format.


        USAGE:
        -----
            bone = lassie.fetch(
                tickers = ["AAPL", "GOOG", "SPY"],
                timeframe="1D",
                start = "2020-5-9",
                end = "2022-5-9"
                )
        
        """
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

    # TODO: Research useful options to start implementing
    # Perhaps request twits from the twitter api
    # maybe there's a news aggregator that can be free.
    def fetch_newspaper(self, tickers, src, start_date, end_date):
        pass 

        



    

    def __doc__(cls):
        return """This is a wrapper for various APIS. Currently just ALPACA"""


if __name__ == "__main__":
    pass 