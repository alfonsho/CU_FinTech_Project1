import numpy as np
import pandas as pd
import hvplot.pandas
import hvplot

from doggie import Doggie

import time as t


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
            # self.generate_random_portfolios()


    def __repr__(self,):
        if self.tickers == None:
            return "Efficient frontier. Please pass some Tickers to agent.tickers"
        else:
            return f"Efficient frontier for tickers {'+'.join(self.tickers)}."


    def set_tickers(self, tickers):
        self.tickers = tickers
        self.get_data()
        self.attention()
        self.calculate_metrics()


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
        # self.annualized_individual_expected_return = relevants.pct_change().mean() * 250

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


    def generate_random_portfolios(self, number_of_portfolios = 5000):
        """
            generates random portfolios
        """

        # if self.tickers == None:
        #     print("Please feed me some tickers")
        #     return None

        portfolios = np.random.uniform(0, 1, (number_of_portfolios, len(self.tickers)))

        sum_of_rows = portfolios.sum(axis=1)

        normalized_portfolios = portfolios / sum_of_rows[:, np.newaxis]

        self.portfolios = pd.DataFrame(normalized_portfolios, columns=self.tickers)

        # Vectorized Calculation of portfolio volatility! F yeah!. it is annualized standard deviation.
        self.portfolios['volatility'] = np.sqrt(self.portfolios.apply(lambda w: w.T@self.cov@w, axis=1)) * np.sqrt(250)

        # Return
        self.portfolios['return'] = self.portfolios[self.tickers].apply(lambda w: w@self.annualized_individual_expected_return, axis=1)

        #SHARPE
        self.portfolios['sharpe_ratio'] = self.portfolios['return'] / self.portfolios['volatility']

        self.portfolios.sort_values('sharpe_ratio', inplace=True)
        return self.portfolios.iloc[-1]


    def display_plot(self, ):
        plot = self.portfolios.hvplot.scatter(  x='volatility', 
                                                y='return', 
                                                grid=True,
                                                hover_cols = list(self.portfolios.columns),
                                                title=" + ".join(self.tickers))
        hvplot.show(plot)


    def validate(self, portfolio):
        """
            given a vector, it ensures no negative components
            scales the vector s.t. it sums to one. 
        """
            
        for i, weight in enumerate(portfolio):
            if weight < 0:
                portfolio[i] = 0 

            
        portfolio /= portfolio.sum()
        return portfolio

        
    def max_sharpe(self, method="gradient_ascent", return_path = False):
        """
            returns the max-sharpe portfolio for a collection of assets
            does not work, just yet. 
        """

        # makes available: annualized
        self.calculate_metrics()

        # Generate 1 portfolio of even weights and calculate initial metrics. 
        # W = np.ones(len(self.tickers)) / len(self.tickers)
        W = np.random.uniform(0, 1, len(self.tickers)) 

        W = np.array([0.283, 0.278, 0.261, 3.36e-2, 1.1e-2, 0.133])
        W = self.validate(W)

        var = W.T @ self.cov @ W
        vol = np.sqrt(var) * np.sqrt(250)
        portfolio_return = W @ self.annualized_individual_expected_return

        S = []
        S.append(portfolio_return / vol)

        pct_chg = 10000

        for i in range(4000):

            # Forward pass (Compute sharpe ratio + relevant components)

            var = W.T @ self.cov @ W
            vol = np.sqrt(var) * np.sqrt(250)

            portfolio_return = W @ self.annualized_individual_expected_return

            S_i = portfolio_return / vol


            # evaluate gradients
            # Volatility's component first: 
            # dvoldw = (np.sqrt(250) / np.sqrt(var)) * (W @ self.cov) 
            # dSdvol = -portfolio_return / vol**2 
            # # Chain rule
            # dSdw_vol = dSdvol * dvoldw

            # # Now Return component
            # dSdr = portfolio_return
            # drdw = self.annualized_individual_expected_return
            # # Chain rule
            # dSdw_ret = dSdr * drdw

            # # Join them 
            # gradS = dSdw_ret + dSdw_vol


            gradS = (2*self.annualized_individual_expected_return.T - W@self.cov)


            # take a step in the direction of gradient
            eta = 0.3
            W += eta * gradS

            # Normalize
            W = self.validate(W)

            # evaluate for stopping condition
            pct_chg = (S_i - S[-1]) / S[-1]
            # print(S_i)
            if pct_chg <= -0.001:
                print("is this running?")

                self.W = W

                if return_path == True:
                    return S, W
                else:
                    return W
            else:
                S.append(S_i)


    def random_tickers(self, n, set_tickers=True):
        """
            selects random tickers from all_tickers.csv
        """
        tickers = pd.read_csv("all_tickers.csv", index_col="Unnamed: 0")
        choices = np.random.choice(tickers['symbol'], n)

        if set_tickers == True:
            self.set_tickers(choices)
        return choices


    def get_ticker_info(self, tickers):
        alltickers = pd.read_csv('all_tickers.csv', index_col='symbol')

        alltickers.drop("Unnamed: 0", axis=1, inplace=True)

        df = alltickers.loc[tickers]

        df["ExpectedReturn"] = self.annualized_individual_expected_return

        return df

    def pretty_print(self):
        print("\n### TICKER INFORMATION\n")
        print(self.get_ticker_info(self.tickers))


        print("\n\n# COVARIANCE MATRIX\n")
        print(self.cov)

        print("\n\n# OPTIMAL POSITION\n")
        max = self.generate_random_portfolios()
        print(max)
    

    


# TODO: ADD FUNCTIONALITY TO "WATCH" A PORTFOLIO. 
#       BY "INVESTING" $100,000.00 IN IT. OR A SET AMOUNT

# TODO: Add fucntionality to partition capital into different 
#       portfolios. Say, I have 2,000,000.00 and 5 isolated portfolios

# TODO: Add presentation capabilities. a pretty print if you will
#       for apartifular portfolio present the info on the tickers
#       followed by the portfolio covariance matrix and finally
#       the portfolio itself. 


if __name__ == "__main__":

    portfolio = efficientFrontier()

    time = t.time()
    tickers = portfolio.random_tickers(7)
    portfolio.set_tickers(tickers)
    portfolio.pretty_print()
    print(t.time()-time)


    

