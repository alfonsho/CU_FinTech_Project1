import numpy as np
import pandas as pd

from doggie import Doggie


class efficientFrontier:
    """
        given a set of tickers, this explores the efficient frontier. 
    """

    def __init__(self, tickers=None):
        self.tickers = tickers
        if self.tickers is not None:
            self.get_data()
            self.attention() # wrangles data so it can be processed. 
            self.calculate_metrics() # calculates statistical metrics like covariance and correlation. 


    def __repr__(self,):
        if self.tickers == None:
            return "Efficient frontier. Please pass some Tickers to agent.tickers"
        else:
            return f"Efficient frontier for tickers {'+'.join(self.tickers)}."


    def set_tickers(self, tickers):
        self.tickers = tickers


    def get_data(self,):
        """
            Uses Doggie to Fetch data from 5 years ago until today. 
        """

        if self.tickers is None:
            print("Please set some tickers using the agent.set_tickers(tickers) method")
            return None 

        end = str(pd.Timestamp.now())[:10]
        start = str(pd.Timestamp.now() - pd.Timedelta(365*5, 'days'))[:10]
        
        doggo = Doggie()

        data = doggo.fetch(tickers=self.tickers,
                    timeframe="1D",
                    start=start,
                    end=end,
                    )

        self.data = data



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

        if overwrite_data == True:
            if method == "log_returns":
                self.data = relevants.pct_change().apply(lambda x: np.log(1+x))
        else:
            return relevants


    def calculate_covariance_matrix(self):
        """
        
        """
        self.cov = self.data.cov()

    def calculate_correlation_matrix(self):
        self.corr = self.data.corr()


    def calculate_metrics(self,):
        self.calculate_covariance_matrix()
        self.calculate_correlation_matrix()


    def generate_random_portfolios(self, number_of_portfolios = 10000):
        """
            generates random portfolios
        """

        if self.tickers == None:
            print("Please feed me some tickers")
            return None

        portfolios = np.random.uniform(0, 1, (number_of_portfolios, len(self.tickers)))

        sum_of_rows = portfolios.sum(axis=1)

        normalized_portfolios = portfolios / sum_of_rows[:, np.newaxis]

        self.portfolios = pd.DataFrame(normalized_portfolios, columns=self.tickers)

        # Vectorized Calculation of portfolio variance! F yeah!. it is annualized btw. 
        self.portfolios['variance'] = np.sqrt(self.portfolios.apply(lambda w: w.T@self.cov@w, axis=1)) * np.sqrt(250)

        # Return
        self.portfolios['return'] = self.portfolios[self.tickers].apply(lambda w: w@self.annualized_individual_expected_return, axis=1)


        return self.portfolios




        









if __name__ == "__main__":

    neo = efficientFrontier(tickers=['NKE', 'GOOGL', 'ARE', 'GLD', 'PFE', 'MSFT'])

    neo.generate_random_portfolios()

    # this is annualized covariance. 
    # print(np.sqrt(neo.cov*250))

    

    neo.portfolios['sharpe_ratio'] = neo.portfolios['return'] / neo.portfolios['variance']

    print(neo.portfolios.sort_values('sharpe_ratio'))

    print(neo.annualized_individual_expected_return)
