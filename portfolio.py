import numpy as np
import pandas as pd

from doggie import Doggie


class portfolioUtilities:
    """

    """

    def __init__(self):
        pass

    def get_data(self, tickers):
        """
            Uses Doggie to Fetch data from 5 years ago until today. 
        """


        end = str(pd.Timestamp.now())[:10]
        start = str(pd.Timestamp.now() - pd.Timedelta(365*5, 'days'))[:10]
        
        doggo = Doggie()

        data = doggo.fetch(tickers=tickers,
                    timeframe="1D",
                    start=start,
                    end=end,
                    )

        return data

    def attention(self, column="close", overwrite_data=True, method="log_returns"):
        """
        all the data fetched, wrangle it so it only gets the desired attributes per ticker. 

        This instance modifies the self.data from the raw alpaca to the log returns on the close price
        for the portfolios. 

        """

        relevants = []

        for ticker in self.tickers:
            relevants.append(self.data[self.data['symbol'] == ticker][column])

        relevants = pd.concat(relevants, axis=1)
        relevants.columns = self.tickers

        self.annualized_individual_expected_return = relevants.resample('Y').last().pct_change().mean()
        # self.annualized_individual_expected_return = relevants.pct_change().mean() * 250

        if overwrite_data == True:
            if method == "log_returns":
                self.data = relevants.pct_change().apply(lambda x: np.log(1+x))
        else:
            return relevants


    def expected_annual_return(self, weights, returns):
        """calculates annual return given weights and historic returns"""
        pass

    

    def log_return(self, ):
        pass

    def cov(self, weights, cov1):
        pass

    def sharpe_ratio(self, ret, vol):
        pass

    def mean_variance_optimize(self, weights, history)


class portfolio(portfolioUtilities):
    """
    portfolio may have functionality and attributes:
        tickers - attr
        weights - attr
        dollar value - attr
        covariance
        sharpe ratio
        volatility
        historic_prices
        date when position was taken 
        take position
        plot

    """

    def __init__(self, tickers=None):
        self.tickers = tickers
        if self.tickers is not None: 
            self.data = self.get_data(self.tickers)




        


if __name__ == "__main__":
    folio = portfolio(tickers=['AAPL', 'ARE'])

    print(folio.data)





    
