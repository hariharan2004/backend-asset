import pandas as pd
from Technicals.bollinger_bands import calculate_bollinger_bands
from Utils.utils import get_current_price

async def bollinger_signal(data_path):
    signal = pd.DataFrame(columns=["Bollinger Band", "Price"])
    data = pd.read_csv(data_path)

    current_btc_price = await get_current_price()
    if current_btc_price is None:
        print("Error: Could not fetch the current price.")
        return signal 
    try:
        current_btc_price = float(current_btc_price)  # Convert to float
    except ValueError:
        print("Error: Current price is not a valid number.")
        return signal
    data['Start'] = pd.to_datetime(data['Start'])
    data = data.sort_values(by='Start')

    data = calculate_bollinger_bands(data)

    lowerband_price = data['Lower Band'].tail(1).iloc[0]
    print("Lower Band data:", lowerband_price)
    middleband_price = data['Middle Band'].tail(1).iloc[0]
    print("Middle Band data:", middleband_price)
    upperband_price = data['Upper Band'].tail(1).iloc[0]
    print("Upper Band data:", upperband_price)

    if current_btc_price < lowerband_price - lowerband_price * 0.01:
        signal.loc[0, 'Bollinger Band'] = "BUY"
        signal.loc[1, 'Price'] = current_btc_price
    elif current_btc_price > upperband_price + upperband_price * 0.01:
        signal.loc[0, 'Bollinger Band'] = "SELL"
        signal.loc[1, 'Price'] = current_btc_price
    else:
        signal.loc[0, 'Bollinger Band'] = "Neutral"
        signal.loc[1, 'Price'] = 0

    return signal

