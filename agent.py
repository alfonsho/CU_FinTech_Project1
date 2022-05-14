import sys
# from dis import dis
import pandas as pd
import numpy as np

from doggie import Doggie
import hvplot.pandas, hvplot

from MCForecastTools import MCSimulation





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

        self.cov = self.data.cov() * 252


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


        risk = weights@self.cov@weights #* 252 /100

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

        candidates = np.random.uniform(0, 1, (number_of_portfolios, number_of_assets))
        normalized = (candidates.T / candidates.sum(axis=1)).T

        for portfolio in normalized:
   
            portfolios = portfolios.append(self.F(portfolio), ignore_index=True)

        portfolios.drop(portfolios[(portfolios[self.tickers].sum(axis=1) > 1)].index, inplace=True)
        self.portfolios = portfolios


    def r(self, risk, epsilon=0.005):
        rng = self.portfolios[(self.portfolios['risk'] > risk - epsilon) & (self.portfolios['risk'] < risk + epsilon)]
        return rng



    def display_plot(self, ):
        plot = self.portfolios.hvplot.scatter(  x='risk', 
                                                y='return', 
                                                grid=True,
                                                hover_cols = list(self.portfolios.columns),
                                                title=" + ".join(self.tickers))
        hvplot.show(plot)




    def save_plot(self):
        plot = self.portfolios.hvplot.scatter(  x='risk', 
                                                y='return', 
                                                grid=True,
                                                hover_cols = list(self.portfolios.columns),
                                                title=" + ".join(self.tickers))


        filename = './resources/' + '+'.join(self.tickers) + ".html"

        hvplot.save(plot, filename=filename)



    def there_is_no_spoon(self, plot='save'):


        self.attention()
        self.random_portfolios()


        if plot == "show":
            self.display_plot()

        elif plot == "save":
            self.save_plot()




    def oracle(self):
        """
        simulates performs simulation based on the found portfolios. 
        
        """
        pass







        






if __name__ == "__main__":


    if len(sys.argv)>1:
        
        print(sys.argv)


    """ARE           0.100969
    GLD           0.140147
    LLY           0.041370
    MSFT          0.144150
    PFE           0.055741
    TSLA          0.480805
    WMT           0.036818"""



    tank = Doggie()

    lady_in_red = tank.fetch(
                tickers = ["ARE", 
                            "GLD", 
                            "LLY", 
                            "MSFT", 
                            "PFE", 
                            'TSLA', 
                            'WMT'],
                timeframe="1D",
                start = "2017-5-9",
                end = "2022-5-13"
                )

    print(lady_in_red)

    separate = [lady_in_red[lady_in_red['symbol'] == symbol] for symbol in lady_in_red['symbol'].unique()]
    data = pd.concat(separate, axis=1,join="inner", keys = lady_in_red['symbol'].unique())


    sim = MCSimulation( portfolio_data = data,
                weights=[0.100969,
                0.140147,
                0.041370,
                0.144150,
                0.055741,
                0.480805,
                0.036818
                        ],
                num_simulation=1000,
                    num_trading_days=252*3
    )

    sim.calc_cumulative_return()

    sim.plot_simulation()

    # neo = Agent(lady_in_red)

    # neo.there_is_no_spoon(plot='show')

    # print(sys.argv)


    

    






