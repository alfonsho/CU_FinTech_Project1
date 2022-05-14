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
        ## I know... this is dirty... change it into something cleaner
        # Problem description: self.data is modified by the self.attention method
        # which then is used by the rest of the class. I could rewrite all of that
        # or just endure this short code fart. 
        self.asset_DataFrame = asset_DataFrame
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

    def select_portfolio_by_risk(self, level=0, as_list=False):
        lower = self.portfolios['risk'].min()
        upper = self.portfolios['risk'].max()

        steps = np.linspace(lower, upper, 3)

        # TODO: rewrite the following fart. It works. it's just smelly. 
        candidate = self.portfolios[np.isclose(self.portfolios['risk'], steps[level], rtol=steps[1]-steps[0])].sort_values('return').iloc[-1]
        
        self.portfolio = candidate

        if as_list == True:
            return list(candidate[self.tickers])

        
        
        return candidate


    def oracle(self, risk=None):
        """
        simulates performs simulation based on the found portfolios. 
        
        """

        if risk == "low":
            risk = self.select_portfolio_by_risk(level=0, as_list=True)

        elif risk == "med":
            risk = self.select_portfolio_by_risk(level=1, as_list=True)

        elif risk == "high":
            risk = self.select_portfolio_by_risk(level=2, as_list=True)

        elif risk == None:
            risk = ""

        separate = [self.asset_DataFrame[self.asset_DataFrame['symbol'] == symbol] for symbol in self.asset_DataFrame['symbol'].unique()]
        data = pd.concat(separate, axis=1,join="inner", keys = self.asset_DataFrame['symbol'].unique())

        sim = MCSimulation(portfolio_data=data,
                            weights=risk,
                            num_simulation=1000,
                            num_trading_days=252*3
                            )

        sim.calc_cumulative_return()

        self.simulation = sim


    def budget_allocation(self, budget, to_csv=False):
        "requires the existence of self.portfolio. "

        budget_allocation = self.portfolio*budget

        if to_csv==True:
            budget_allocation.to_csv("./resources/budget_allocation.csv")

        return budget_allocation







def run(tickers, budget=100000, risk=None):
    """
    generates a payload in resources. 
    """

    tank = Doggie()

    start = str(pd.Timestamp.now())[:10]
    end = str(pd.Timestamp.now() - pd.Timedelta(365*5, 'days'))[:10]

    lady_in_red = tank.fetch(
    tickers = tickers,
            timeframe="1D",
            start = "2017-5-9",
            end = "2022-5-13"
            )


    neo = Agent(lady_in_red)
    neo.there_is_no_spoon(plot='save')

    neo.oracle(risk='high')
    neo.simulation.plot_simulation()

    neo.budget_allocation(budget, to_csv=True)






        






if __name__ == "__main__":


    if len(sys.argv) < 2:
        help = """
        EXAMPLE USAGE: 
            From the command line type:

                % python agent.py --run -tickers=AAPL,MSFT,GLD,PFE,TSLA,WMT -risk=high

            tickers take any tickers in that format. 

            risk can be "low", "med", "high" or simply not provided. 

        OUTPUT:
        ------
            It will generate 3 files to the resources folder. 
                
                - risk return characteristics for the portfolio as an HTML interactive plot. 
                - A plot of a Monte Carlo simulation of the provided assets according to the risk provided
                - A CSV of the selected portfolio allocation valued in USD according to the budget given. 

            if No risk level is provided, the code will run a Monte Carlo with even weights. 
        
        """
        print(help)


        
        print(sys.argv)


    tickers = ["ARE", 
                            "GLD", 
                            "LLY", 
                            "MSFT", 
                            "PFE", 
                            'TSLA', 
                            'WMT']

    # run(tickers, budget, risk)
















    

    






