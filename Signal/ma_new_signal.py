import pandas as pd
from Utils.utils import get_current_price
from Technicals.ma import calculate_ma

async def ma_signals(data_path):
    signal = pd.DataFrame(columns=["Moving Average"])
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

    previous_btc_price_close = data['Close'].iloc[1]  # Get the last closing price
    closing_time = "00:20:00"
    
    data['Start'] = pd.to_datetime(data['Start'])
    data = data.sort_values(by='Start')
    data = calculate_ma(data)
    
    ma_values = {
        "ma200": data["200-Day MA"].iloc[-1],
        "ma100": data["100-Day MA"].iloc[-1],
        "ma50": data["50-Day MA"].iloc[-1]
    }
    
    print("Current BTC Price:", current_btc_price)
    print("200 D MA:", ma_values["ma200"])
    print("100 D MA:", ma_values["ma100"])
    print("50 D MA:", ma_values["ma50"])
    print("Previous Closing Price:", previous_btc_price_close)

    def set_signal(condition, label):
        if condition:
            signal.loc[0, 'Moving Average'] = label

    # Prioritize signals based on proximity to MAs
    if current_btc_price < ma_values["ma200"]:
        if previous_btc_price_close < ma_values["ma200"]:
            set_signal(current_btc_price < ma_values["ma200"], "SELL-MA200")
            if current_btc_price > ma_values["ma200"] - ma_values["ma200"] * 0.01:
                set_signal(current_btc_price > ma_values["ma100"], "SELL-NEAR-MA200")

    elif current_btc_price < ma_values["ma100"]:
        if previous_btc_price_close < ma_values["ma100"]:
            set_signal(current_btc_price < ma_values["ma100"], "SELL-MA100")
            if current_btc_price > ma_values["ma100"] - ma_values["ma100"] * 0.01:
                set_signal(current_btc_price > ma_values["ma50"], "SELL-NEAR-MA100")
    
    elif current_btc_price < ma_values["ma50"]:
        if previous_btc_price_close < ma_values["ma50"]:
            set_signal(current_btc_price < ma_values["ma50"], "SELL-MA50")
            if current_btc_price > ma_values["ma50"] - ma_values["ma50"] * 0.01:
                set_signal("BUY-NEAR-MA50", "BUY-NEAR-MA50")

    # For buying conditions, we can check proximity to the MAs as well
    if current_btc_price > ma_values["ma200"]:
        if previous_btc_price_close < ma_values["ma200"]:
            set_signal(current_btc_price > ma_values["ma200"] + ma_values["ma200"] * 0.01, "BUY-MA200")
    
    elif current_btc_price > ma_values["ma100"]:
        if previous_btc_price_close < ma_values["ma100"]:
            set_signal(current_btc_price > ma_values["ma100"] + ma_values["ma100"] * 0.01, "BUY-MA100")

    elif current_btc_price > ma_values["ma50"]:
        if previous_btc_price_close < ma_values["ma50"]:
            set_signal(current_btc_price > ma_values["ma50"] + ma_values["ma50"] * 0.01, "BUY-MA50")

    return signal
