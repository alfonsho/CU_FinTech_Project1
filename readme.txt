
        EXAMPLE USAGE: 

        .ENV SETUP: 
        ----------
            1) Fetch your Alpaca Credentials, 
            2) Put them into the included file named: your.env 
            3) rename the your.env file to .env


        EXAMPLE EXECUTION:
        -------
            From the command line type:

                % python agent.py --run -tickers=AAPL,MSFT,GLD,PFE,TSLA,WMT -risk=high

            - tickers take any tickers in that format. 
            - risk can be "low", "med", "high" or simply not provided. 


        OUTPUT:
        ------
            It will generate 3 files to the resources folder. 
                
                - risk return characteristics for the portfolio as an HTML interactive plot. 
                - A plot of a Monte Carlo simulation of the provided assets according to the risk provided
                - A CSV of the selected portfolio allocation valued in USD according to the budget given. 

            if No risk level is provided, the code will run a Monte Carlo with even weights. 
        
