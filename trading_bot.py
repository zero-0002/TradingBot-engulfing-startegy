import pandas as pd
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest, TakeProfitDetails, StopLossDetails
from oanda_candles import Pair, Gran, CandleClient
from apscheduler.schedulers.blocking import BlockingScheduler
import data_preparation as dp  # Importing functions from data_preparation.py
import config  # Importing configurations from config.py

# Function to retrieve the last n candles from the OANDA market
def get_candles(n):
    client = CandleClient(config.access_token, real=False)
    collector = client.get_collector(Pair.EUR_USD, Gran.M15)
    candles = collector.grab(n)
    return candles

def trading_job():
    """
    Main trading function that performs the following tasks:
    1. Retrieve the latest market candles.
    2. Convert candle data to a pandas DataFrame.
    3. Generate a trading signal based on the engulfing pattern.
    4. Execute a market order based on the generated signal with specified stop loss and take profit levels.
    """
    
    # Step 1: Retrieve the last 3 candles from the market.
    candles = get_candles(3)
    
    # Step 2: Convert candle data to a pandas DataFrame with Open, Close, High, and Low columns.
    dfstream = pd.DataFrame(columns=['Open','Close','High','Low'])
    for i, candle in enumerate(candles):
        dfstream.loc[i, ['Open', 'Close', 'High', 'Low']] = [float(str(candle.bid.o)), float(str(candle.bid.c)), float(str(candle.bid.h)), float(str(candle.bid.l))]
    dfstream = dfstream.astype(float)
    
    # Step 3: Generate a trading signal using the signal_generator function from data_preparation.py.
    # The function analyzes the last two closed candles and returns a signal.
    signal = dp.signal_generator(dfstream.iloc[:-1, :])

    # Step 4: Execute a market order based on the signal with specified stop loss and take profit levels.
    # Calculate the stop loss and take profit levels based on the previous candle's range.
    previous_candleR = abs(dfstream['High'].iloc[-2] - dfstream['Low'].iloc[-2])
    SLTPRatio = 2.0
    SLBuy = dfstream['Open'].iloc[-1] - previous_candleR
    SLSell = dfstream['Open'].iloc[-1] + previous_candleR
    TPBuy = SLBuy + previous_candleR * SLTPRatio
    TPSell = SLSell - previous_candleR * SLTPRatio
    
    # Initialize OANDA API client.
    client = API(access_token=config.access_token)

    # If signal is 1 (Sell), execute a selling market order with the calculated stop loss and take profit.
    if signal == 1:
        mo = MarketOrderRequest(instrument="EUR_USD", units=-1000, takeProfitOnFill=TakeProfitDetails(price=TPSell).data, stopLossOnFill=StopLossDetails(price=SLSell).data)
        r = orders.OrderCreate(config.accountID, data=mo.data)
        rv = client.request(r)
        print(rv)

    # If signal is 2 (Buy), execute a buying market order with the calculated stop loss and take profit.
    elif signal == 2:
        mo = MarketOrderRequest(instrument="EUR_USD", units=1000, takeProfitOnFill=TakeProfitDetails(price=TPBuy).data, stopLossOnFill=StopLossDetails(price=SLBuy).data)
        r = orders.OrderCreate(config.accountID, data=mo.data)
        rv = client.request(r)
        print(rv)


# Function to start and schedule the trading bot
def run_bot():
    scheduler = BlockingScheduler()
    # Schedule the trading job with specified cron parameters
    scheduler.add_job(trading_job, 'cron', day_of_week='mon-fri', hour='00-23', minute='1,16,31,46', start_date='2023-01-12 12:00:00', timezone='America/Chicago')
    scheduler.start()  # Start the scheduler

# Run the bot if the script is executed
if __name__ == "__main__":
    run_bot()
