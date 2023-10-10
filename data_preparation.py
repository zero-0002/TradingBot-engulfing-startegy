import yfinance as yf
import pandas as pd

# Function to download historical data from Yahoo Finance
# Start date and end date need to be specified
def download_data(start_date, end_date):
    # Replace "EURUSD=X" with your preferred trading pair.
    # You can also replace the interval your preferred interval. Refer to yfinance documentation.
    dataF = yf.download("EURUSD=X", start=start_date, end=end_date, interval="15m")
    return dataF

# Function to generate trading signals based on the data
# The function uses the last two rows of the data to generate a signal
def signal_generator(df):
    open = df.Open.iloc[-1]
    close = df.Close.iloc[-1]
    previous_open = df.Open.iloc[-2]
    previous_close = df.Close.iloc[-2]
    
    # Bearish engulfing pattern detection
    if (open > close and 
        previous_open < previous_close and 
        close < previous_open and
        open >= previous_close):
        return 1  # Return 1 for a sell signal
    
    # Bullish engulfing pattern detection
    elif (open < close and 
          previous_open > previous_close and 
          close > previous_open and
          open <= previous_close):
        return 2  # Return 2 for a buy signal
    
    # No clear pattern detected
    else:
        return 0  # Return 0 if no clear signal is identified