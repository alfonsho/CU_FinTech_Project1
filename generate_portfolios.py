import numpy as np
import pandas as pd

from doggie import Doggie


class Agent:

    def __init__(self, tickers=None):
        self.tickers = tickers

    def set_tickers(self, tickers):
        self.tickers = tickers

    def __repr__(self,):
        if self.tickers == None:
            return "Efficient frontier. Please pass some Tickers to agent.tickers"
        else:
            return f"Efficient frontier for tickers {'+'.join(self.tickers)}."

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

        self.portfolios = pd.DataFrame(normalized_portfolios, columns=tickers)

        









if __name__ == "__main__":

    neo = Agent()
    neo.set_tickers(['AAPL', 'TSLA', 'MSFT', 'ARE'])

    doggo = Doggie()

    data = doggo.fetch(tickers=neo.tickers,
    timeframe="1D",
    start="2020-05-10",
    end="2022-05-10",
    )





    print(data)
