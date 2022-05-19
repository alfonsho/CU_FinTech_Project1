import pandas as pd
import numpy as np
import os 
import requests
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import json



class Doggie:
    def __init__(self, api="alpaca"):
        load_dotenv()

        self.api = api
        if self.api == "alpaca":
            
            self.alpaca_api_key = os.getenv("ALPACA_API_KEY")
            self.alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
            self.alpaca = tradeapi.REST(self.alpaca_api_key,
                                        self.alpaca_secret_key,
                                        api_version="V2")

        if self.api == "polygon.io":
            self.polygon_api_key = os.getenv("POLYGON_API_KEY")
            self.base_url = "https://api.polygon.io"

                


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
    # Perhaps request tweets from the twitter api
    # maybe there's a convenient news aggregator.
    def fetch_newspaper(self, tickers, src, start_date, end_date):
        pass 

        
    def polygon_aggregates(self, stocksTicker, multiplier, timespan, fm, to):
        """
            Get aggregate bars for a stock over a given date range in custom time window sizes. 
            For example, if timespan = minute and multiplier = 5 then 5-minute bars will be returned.

            https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2021-07-22/2021-07-22?adjusted=true&sort=asc&limit=120&apiKey=*****REDACTED*****
        """
        endpoint = f"/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{fm}/{to}?adjusted=true&sort=asc&apiKey={self.polygon_api_key}"
        response = requests.get(self.base_url + endpoint)

        return response

    def polygon_grouped_daily(self, date):
        """
        Get the daily open, high, low, and close (OHLC) for the entire stocks/equities markets.
        https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2020-10-14?adjusted=true&apiKey=******REDACTED*******
        
        """
        endpoint = f'/v2/aggs/grouped/locale/us/market/stocks/{date}?apiKey={self.polygon_api_key}'
        response = requests.get(self.base_url + endpoint)

        df = pd.DataFrame(response.json()['results'])

        return df



    def keep(self):
        """
        
        """





if __name__ == "__main__":

    lassie = Doggie(api="polygon.io")

    data = lassie.polygon_grouped_daily("2022-05-18")

    print(data)
    
