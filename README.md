# Trading Bot

## Overview
This Trading Bot is a Python application designed for automating trading strategies. It executes trades on the OANDA platform. The bot downloads historical forex data, generates trading signals based on candlestick patterns, and places market orders. It primarily operates based on the Engulfing candlestick pattern, a reliable indicator frequently used in trading.

#### Engulfing Pattern Strategy:
- **Analyzing Previous Candles:**
  - The bot continuously observes the financial market, examining the previous two candles in a given timeframe.
  - It analyses these candles, looking for either a Bullish or Bearish Engulfing pattern to make trading decisions.
  - An engulfing pattern is a strong reversal signal. A Bullish Engulfing indicates the reversal of a downtrend, while a Bearish Engulfing suggests the reversal of an uptrend.

- **How the Engulfing Pattern is Identified:**
  - *Bearish Engulfing:*
    - The opening price of the current (latest) candle is higher than its closing price (it's a red candle).
    - The opening price of the previous candle is lower than its closing price (it's a green candle).
    - The closing price of the current candle is lower than the opening price of the previous candle.
    - The opening price of the current candle is higher or equal to the closing price of the previous candle.
  - *Bullish Engulfing:*
    - The opening price of the current candle is lower than its closing price (it's a green candle).
    - The opening price of the previous candle is higher than its closing price (it's a red candle).
    - The closing price of the current candle is higher than the opening price of the previous candle.
    - The opening price of the current candle is lower or equal to the closing price of the previous candle.

#### Trade Execution:
- **Determining Stop Loss and Take Profit:**
  - Stop Loss (SL) and Take Profit (TP) levels are crucial parameters set before executing trades to manage risks efficiently.
  - The bot calculates the Stop Loss level based on the range (high-low) of the second to last candle.
  - The Take Profit level is determined by multiplying the Stop Loss distance by a predefined Risk-Reward Ratio (in this case, 2.0, meaning the Take Profit is set to twice the distance of the Stop Loss from the entry point).
  - For a buying order: 
    - The SL is set below the opening price of the current candle by the amount calculated for Stop Loss.
    - The TP is set above the opening price by the amount calculated for Take Profit.
  - For a selling order:
    - The SL is set above the opening price of the current candle by the amount calculated for Stop Loss.
    - The TP is set below the opening price by the amount calculated for Take Profit.

- **Trade Size Determination:**
  - The trading bot executes trades with a fixed size of 1000 units per order (This size is hardcoded but can be adjusted based on user preference and risk management rules).

Through these mechanisms, the Trading Bot systematically analyzes market data, identifies profitable trading signals based on the Engulfing Pattern strategy, and executes trades while managing risks with predetermined Stop Loss and Take Profit levels. The end goal is to automate the trading process efficiently, minimizing human intervention and emotional decision-making, and potentially increasing profitability in trading endeavors.


## Structure
- `config.py`: Holds configuration settings, including API token and account ID.
- `data_preparation.py`: Contains functions for data downloading and signal generation.
- `trading_bot.py`: Contains the main trading logic and functions to execute trades.

## Prerequisites
- Python 3.x
- Required Python packages: `yfinance`, `pandas`, `apscheduler`, `oandapyV20`, and any others required by your system.

## Setup
1. Clone this repository or download the source files.
2. Navigate to the project directory.
3. Install the required Python packages using pip:
    ```
    pip install -r requirements.txt
    ```
4. Add your OANDA API token and account ID to the `config.py` file.

## Usage

1. Install required Python packages:
    ```
    pip install -r requirements.txt
    ```
2. Run the trading bot:
    ```
    python trading_bot.py
    ```
3. The bot will start scheduling the trading jobs based on the defined cron schedule in `trading_bot.py`.

## Functionality

### `config.py`
- **`access_token`**: Your OANDA access token.
- **`accountID`**: Your OANDA account ID.

### `data_preparation.py`
- **`download_data(start_date, end_date)`**: Downloads historical forex data between specified start and end dates. Replace the trading pair in the function call if needed.
- `start_date`: The start date of the data to be downloaded.
- `end_date`: The end date of the data to be downloaded.
- `interval`: The timeframe interval for the candlesticks being downloaded. I chose 15 minu

- **`signal_generator(df)`**: Generates trading signals based on the data. It analyzes the last two candles of the data, detects engulfing patterns and returns a signal.
- `df`: The dataframe containing market data. 
- Returns `1` for sell, `2` for buy, and `0` for no action.

### `trading_bot.py`
- **`get_candles(n)`**: Retrieves the last `n` candles from the OANDA market.
- `n`: Number of candles to retrieve.

- **`trading_job()`**: Main trading function that downloads data, generates signals, and executes trades based on signals. Stop loss and take profit values are set within this function.

- **`run_bot()`**: Initializes and starts the scheduler to run the trading bot at specified times. The bot is scheduled to run on weekdays every 15 minutes during market hours.

## Customization
- You can modify the trading pair, date range, and other parameters in the respective function calls and configurations within the source files.


## Disclaimer
Trading involves risks and this bot is provided without any warranty. Use it at your own risk and discretion. Always test any trading algorithm with a demo account before using it in a live trading environment.
