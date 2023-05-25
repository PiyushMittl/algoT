
import time
from kiteconnect import KiteConnect

# Initialize Zerodha API
api_key = "<your_api_key>"
access_token = "<your_access_token>"
kite = KiteConnect(api_key=api_key)

#print(kite.login_url())

data = kite.generate_session("<your_token>",access_token)
print(data)

kite.set_access_token(data["access_token"])


# Define moving average crossover strategy
def moving_average_crossover(symbol, interval, short_period, long_period):

    to_date='2023-05-23'
    from_date='2023-05-22'
    # Get historical data
    historical_data = kite.historical_data(symbol, interval=interval, from_date=from_date, to_date=to_date)

    # Calculate short and long moving averages
    short_ma = sum([candle['close'] for candle in historical_data[-short_period:]]) / short_period
    long_ma = sum([candle['close'] for candle in historical_data[-long_period:]]) / long_period

    # Generate buy/sell signal
    if short_ma > long_ma:
        return 'BUY'
    elif short_ma < long_ma:
        return 'SELL'
    else:
        return 'HOLD'

# Main trading loop
while True:
    try:
        # Get buy/sell signal
        #signal = moving_average_crossover('408065', '15minute', 10, 20)
        signal = moving_average_crossover('408065', '15minute', 15, 200)

        # Place order if signal is 'BUY' or 'SELL'
        if signal in ['BUY', 'SELL']:
            order = kite.place_order(variety='regular',
                                     tradingsymbol='INFY',
                                     exchange='NSE',
                                     transaction_type=signal,
                                     quantity=1,
                                     order_type='MARKET',
                                     product='MIS')

            print("Placed order:", order)
        else:
            print("No signal. Holding position.")

        # Sleep for 1 minute before checking again
        time.sleep(60)

    except Exception as e:
        print("An error occurred:", str(e))
        break
