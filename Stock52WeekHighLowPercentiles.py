import pandas as pd
import yfinance as yf

class Stock52WeekHighLowPercentiles:
    """
    This class uses yfinance and pandas to calculate the 52 week highs and lows for a stock at the date level. 
    It also calculates where the price is relative to the 52 week high low at the date level.
    """
    def __init__(self, ticker, start_date, end_date):
        """
        Initialize the class.
        
        Parameters
        ----------
        ticker : str
            The stock ticker to be analysed.
        start_date : str
            The start date for the analysis.
        end_date : str
            The end date for the analysis.
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
    
    def get_data(self):
        """
        Get the stock data from yfinance.
        
        Returns
        -------
        data : pandas.DataFrame
            The stock data from yfinance
        """
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        return self.data
    
    def calculate_52week_percentiles(self):
        """
        Calculate the 52 week highs and lows and where the price is relative to the 52 week high low.
        
        Returns
        -------
        data : pandas.DataFrame
            The stock data from yfinance with the added 52 week high, low and percentile columns.
        """
        if self.data is None:
            self.get_data()
        self.data['52wk_high'] = self.data['Close'].rolling(window=252).max()
        self.data['52wk_low'] = self.data['Close'].rolling(window=252).min()
        self.data['52wk_percentile'] = (self.data['Close'] - self.data['52wk_low']) / (self.data['52wk_high'] - self.data['52wk_low'])
        self.data['52wk_percentile_21_sma'] = self.data['52wk_percentile'].rolling(window=21).mean()

        self.data['ticker'] =  self.ticker
        self.data.dropna(inplace=True)
        return self.data