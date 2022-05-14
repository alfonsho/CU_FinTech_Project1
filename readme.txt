
        EXAMPLE USAGE: 

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
        
