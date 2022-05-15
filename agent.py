import argparse
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

        

        portfolios = np.random.uniform(0, 1, (number_of_portfolios, number_of_assets))
        sum_of_rows = portfolios.sum(axis=1)
        normalized = portfolios / sum_of_rows[:, np.newaxis]

        portfolios = pd.DataFrame(columns=self.tickers)

        for portfolio in normalized:


   
            portfolios = portfolios.append(self.F(portfolio), ignore_index=True)

        # portfolios.drop(portfolios[(portfolios[self.tickers].sum(axis=1) > 1)].index, inplace=True)
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


        # TODO: Rewrite to include when the user inputs no risk. in other words
        # allow the user to query the evenly distributed portfolio. The rest of the code runs fine
        # it's just this function which decides to use the level 0 portfolio instead of the evenly one. 
        self.portfolio = candidate

        if as_list == True:
            return list(candidate[self.tickers])

        
        
        return candidate


    def oracle(self, risk=None):
        """
        simulates performs simulation based on the found portfolios. 
        
        """

        input_validation = ['low', "med", "high", None, ""]
        if risk not in input_validation:
            raise TypeError

        if risk == "low":
            risk = self.select_portfolio_by_risk(level=0, as_list=True)

        elif risk == "med":
            risk = self.select_portfolio_by_risk(level=1, as_list=True)

        elif risk == "high":
            risk = self.select_portfolio_by_risk(level=2, as_list=True)

        elif risk == None or risk == '':
            self.select_portfolio_by_risk(level=0)
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

    neo.oracle(risk=risk)
    neo.simulation.plot_simulation()

    neo.budget_allocation(budget, to_csv=True)




def parse_argv(argv):



    d = {}

    for arg in argv:
        if "-tickers" in arg:
            payload = arg.split("=")[1]
            if "," in payload:
                d['tickers'] = arg.split("=")[1].split(',')
            else:
                d['tickers'] = [payload]

        if "-risk" in arg:
            payload = arg.split("=")[1]
            if payload.isnumeric():
                d['risk'] = int(payload)
            elif type(payload) == str or payload is None:
                d['risk'] = payload
        
        elif "-risk" not in arg:
            d['risk'] = None

        if "-budget" in arg:
            payload = arg.split("=")[1]
            d['budget'] = float(payload)

        elif '-budget' not in arg:
            d['budget'] = 100000

    

    return d








        






if __name__ == "__main__":


    if len(sys.argv) < 2:
        
        with open("readme.txt", 'r') as f:
            help = f.read()

        print(help)
    else:
        
        d = parse_argv(sys.argv)

        run(budget=d['budget'], risk=d['risk'], tickers=d['tickers'])


















    

    






