import pandas_datareader.data as web
from datetime import datetime,timedelta
import pandas as pd
from ta import rsi

def rsi(sym):
    window_length = 14
    start = datetime(2015, 2, 9)
    end = datetime.today()
    # Get data
    data = web.DataReader(sym, 'iex', start, end)
    # Get just the close
    close = data['close']
    # Get the difference in price from previous step
    delta = close.diff()
    # Get rid of the first row, which is NaN since it did not have a previous
    # row to calculate the differences
    delta = delta[1:]

    # Make the positive gains (up) and negative gains (down) Series
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    # Calculate the EWMA
    #pd.
    # roll_up1 = up.ewm(min_periods  = window_length)
    # roll_down1 = pd.ewm(down.abs(), window_length)
    #
    # # Calculate the RSI based on EWMA
    # RS1 = roll_up1 / roll_down1
    # RSI1 = 100.0 - (100.0 / (1.0 + RS1))

    # Calculate the SMA

    roll_up2 = up.rolling(window_length).mean()
    #print(roll_up2)
    roll_down2 = down.rolling(window_length).mean()
    print(roll_down2)

    # Calculate the RSI based on SMA
    RS2 = roll_up2 / roll_down2
    RSI2 = 100.0 - (100.0 / (1.0 + RS2))
    return (RSI2[-1])



#start = datetime(2015, 2, 9)
start = datetime.today() - timedelta(days=55)
end = datetime.today()

f = web.DataReader('GOOG', 'iex', start, end)

print(f.tail())
print(rsi('FB'))

