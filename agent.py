
import pandas as pd
import numpy as np

from doggie import Doggie
import hvplot.pandas, hvplot



class Agent:
    '''
    3 fundamental general principles for agents. 
        - Attention: gets the data into usable form
        - Intention: minimize error, maximize utility, etc
        - Cognition: runs a particular process to find the action(s) with the belief it will maximize intention.
        - Action: returns optimal action(s)
    '''

    def __init__(self, asset_DataFrame):
        self.data = asset_DataFrame
        self.tickers = asset_DataFrame['symbol'].unique()

        self.keys = list(self.tickers) + ['risk', 'return']


    def attention(self):
        """
            get the asset_DataFrame from its raw state 
                currently an alpaca timestamp|open|high|low|close|volume|trade_count|vwap|symbol
            into a desired state
                in this case I want 
                timestamp|ticker|

        """
        closes = []
        for ticker in self.tickers:
            closes.append(self.data[self.data["symbol"]==ticker]['close'])

        closes = pd.concat(closes, axis=1)
        self.data = closes.pct_change()
        self.data.columns = self.tickers


    def F(self, weights):
        """
        Inputs: 
        ------  
            weights: portfolio weights. 

        Outputs:
        -------
            a 2 vector:
                risk
                return


        """

        cov = self.data.cov() * 252 #annualized
        risk = weights@cov@weights
        ret = self.data.mean(axis=0)*252@weights


        values = list(weights)
        values.append(risk)
        values.append(ret)


        d = {}
        for i, key in enumerate(self.keys):
            d[key] = values[i]


        s = pd.Series(d)



        return s



    def random_portfolios(self, number_of_portfolios=1000):
        """
        creates N random possible portfolios of size M where M is the number of assets in the asset dataframe. 

        returns a matrix where 

                the rows are portfolios, the columns are allocations for asset i 
        """


        number_of_assets = len(self.tickers)

        portfolios = pd.DataFrame(columns=self.keys)

        for portfolio in range(number_of_portfolios):

            unnorm = np.random.uniform(0, 1, number_of_assets)
            weights = unnorm/unnorm.sum()

            portfolios = portfolios.append(self.F(weights), ignore_index=True)


        self.portfolios = portfolios



    def plot(self):
        plot = self.portfolios.hvplot.scatter(  x='risk', 
                                                y='return', 
                                                grid=True,
                                                hover_cols = list(self.portfolios.columns))
        hvplot.show(plot)

        

    def there_is_no_spoon(self, display=True):
        self.attention()
        self.random_portfolios()
        if display == True:
            self.plot()

        





    def __doc__(cls):
        s = """
        This particular agent will receive a collection 
        of n assets in a pandas time-series DataFrame. 
        
        it generates M portfolios of random allocations
        of the assets in said portfolio. 

        places them in risk-return space. 

        plots them. 

        Given desired return, chooses portfolio with
        closest return with the least risk.

        Given desired risk, chooses portfolio with the 
        max return, given 

        """

        return s




if __name__ == "__main__":

    tank = Doggie()

    lady_in_red = tank.fetch(
                tickers = ["AAPL", "MSFT", "GLD"],
                timeframe="1D",
                start = "2015-5-9",
                end = "2022-5-9"
                )

    neo = Agent(lady_in_red)
    neo.there_is_no_spoon()


