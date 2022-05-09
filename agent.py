from re import S
import pandas as pd
import numpy as np



class Agent:

    def __init__(self, asset_DataFrame):
        pass

    # def 

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
    neo = Agent(2)
    Agent.__doc__(2)

