
 
    agent.py
        known issues: The computation of volatility needs to be andjusted. 
 
        EXAMPLE USAGE : 

        .ENV SETUP: 
        ----------
            1) Fetch your Alpaca Credentials, 
            2) Put them into the included file named: your.env 
            3) rename the your.env file to .env


        EXAMPLE EXECUTION:
        -------
            From the command line type:

                % python agent.py --run -tickers=AAPL,MSFT,GLD,PFE,TSLA,WMT -risk=high -budget=1000000

            - tickers take any tickers in that format. This is the only obligatory input. 
            - risk can be "low", "med", "high" or simply not provided. 
            - budget can be any integer or if not provided, 10,000 will be assumed.


        OUTPUT:
        ------
            It will generate 3 files to the resources folder. 
                
                - risk return characteristics for the portfolio as an HTML interactive plot. 
                - A plot of a Monte Carlo simulation of the provided assets according to the risk provided
                - A CSV of the selected portfolio allocation valued in USD according to the budget given. 

            if No risk level is provided, the code will run a Monte Carlo with even weights. 


        

    efficient_frontier.py
        This module has a better implementation of the return-volatility calculation. 
        Also requires your alpaca credentials in a .env file. 

        EXAMPLE USAGE : 

            from efficient_frontier import efficientFrontier

            # Fetches data by itself 
            neo = efficientFrontier(tickers=['MSFT', 'GLD', 'LLY', 'ARE', 'SPY', 'BND'])

            # This function generates 5000 of portfolios of the provided assets. 
            # Returns the one with the highest sharpe ratio. Which is unlikely to be the
            # actual very best. but it's pretty good. 
            max_sharpe = neo.generate_random_portfolios()

            # This plots the portfolios generated using hvplot in the volatility-return space
            neo.display_plot()



        ** New!! 
        efficientFrontier.pretty_print()

            produces something like this: 

                ### TICKER INFORMATION

                                        company_name                                  industry    market_cap  ExpectedReturn
                symbol
                EDUC         Educational Development                              Distributors  4.192000e+07       -0.040854
                HRMY    Harmony Biosciences Holdings                             Biotechnology  2.240000e+09        0.081088
                EZGO               EZGO Technologies                     Recreational Vehicles  1.213000e+07       -0.412752
                SSNT          SilverSun Technologies                                  Software  1.289000e+07        0.043114
                FSRX          FinServ Acquisition II                        Blank Check / SPAC  3.757200e+08        0.006154
                MNST                Monster Beverage                                 Beverages  4.708000e+10        0.098330
                OIIM           O2Micro International  Semiconductors & Semiconductor Equipment  8.887000e+07        0.697005


                # COVARIANCE MATRIX

                        EDUC      HRMY          EZGO      SSNT          FSRX      MNST      OIIM
                EDUC  0.001596  0.000136  2.361740e-04  0.000056  2.777730e-06  0.000129  0.000176
                HRMY  0.000136  0.001390  3.680233e-04  0.000171  1.144350e-05  0.000098  0.000142
                EZGO  0.000236  0.000368  4.243398e-03  0.001016 -7.936633e-07  0.000131  0.000763
                SSNT  0.000056  0.000171  1.016368e-03  0.002932 -2.891361e-05  0.000055  0.000065
                FSRX  0.000003  0.000011 -7.936633e-07 -0.000029  2.886448e-05 -0.000001  0.000003
                MNST  0.000129  0.000098  1.311797e-04  0.000055 -1.286485e-06  0.000317  0.000110
                OIIM  0.000176  0.000142  7.625784e-04  0.000065  3.322353e-06  0.000110  0.001561


                # OPTIMAL POSITION

                EDUC            0.116820
                HRMY            0.033802
                EZGO            0.005130
                SSNT            0.010683
                FSRX            0.290296
                MNST            0.085299
                OIIM            0.457971
                volatility      0.315556
                return          0.325694
                sharpe_ratio    1.032128
                Name: 1922, dtype: float64