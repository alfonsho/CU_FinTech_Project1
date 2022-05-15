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



    def attention(self, column="close"):
        """
        all the data fetched, wrangle it so it only gets the desired attributes per ticker. 
        """

        relevants = []

        for ticker in self.tickers:
            relevants.append(self.data[self.data['symbol'] == ticker][column])

        relevants = pd.concat(relevants, axis=1)
        relevants.columns = self.tickers

        print(relevants)


    def generate_random_portfolios(self, number_of_portfolios = 5000):
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

        return self.portfolios

        









if __name__ == "__main__":

    neo = efficientFrontier()
    neo.set_tickers(['AAPL', 'TSLA', 'MSFT', 'ARE'])

    data = neo.get_data()

    neo.attention()



    print(data)
