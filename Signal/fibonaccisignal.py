from Technicals.fibonacci_levels import calculate_fibonacci
import pandas as pd
from Utils.utils import get_current_price

# Common function to generate signals for multiple Fibonacci levels
def generate_signal(fib_levels, prev_above, prev_below, current_btc_price, previous_btc_close, closing_time):
    signal = "Neutral-default"
    current_btc_price_low = min(prev_below.values())
    
    # Check for each Fibonacci level
    for level in fib_levels.keys():
        if level in prev_above and current_btc_price > prev_above[level]:
            if current_btc_price > fib_levels[level] and current_btc_price < fib_levels[level] + fib_levels[level] * 0.02:
                if previous_btc_close < fib_levels[level]:
                    if current_btc_price > fib_levels[level] - fib_levels[level] * 0.01:
                        signal = f"BUY-{level}"
                    elif current_btc_price < fib_levels[level] and closing_time < "10min":
                        signal = f"SELL-{level}"
                    else:
                        signal = f"NEUTRAL-{level}"
                elif previous_btc_close > fib_levels[level]:
                    if current_btc_price_low > fib_levels[level] - fib_levels[level] * 0.02:
                        if current_btc_price > fib_levels[level]:
                            signal = f"BUY-{level}"
                        elif current_btc_price < fib_levels[level] and closing_time < "15min":
                            signal = f"SELL-{level}"
                        else:
                            signal = f"NEUTRAL-{level}"
                else:
                    signal = f"NEUTRAL-{level}"
    
    return signal

async def fib_signal(data_path):
    signal_list = [] 
    data = pd.read_csv(data_path)
    
    current_btc_price = await get_current_price()
    
    if current_btc_price is None:
        return pd.DataFrame(columns=["macro_signal", "recent_signal"])
    
    # Calculating Fibonacci levels
    macro_fib_level, recent_fib_level = calculate_fibonacci(data)

    # Previous BTC data (can be fetched or updated as per your source)
    previous_btc_close = 60313
    closing_time = "10min"
    
    prev_macro_above = {0.5: 61518, 0.75: 62000, 0.786: 61700}
    prev_macro_below = {0.25: 55361, 0.236: 54475}
    prev_recent_above = {0.5: 61818, 0.75: 61950, 0.786: 61750}
    prev_recent_below = {0.25: 57728, 0.236: 57498}
    
    # Generate macro signal using the common function
    macro_signal = generate_signal(
        macro_fib_level, prev_macro_above, prev_macro_below,
        current_btc_price, previous_btc_close, closing_time
    )
    
    # Generate recent signal using the common function
    recent_signal = generate_signal(
        recent_fib_level, prev_recent_above, prev_recent_below,
        current_btc_price, previous_btc_close, closing_time
    )
    
    # Append signals
    signal_list.append({"macro_signal": macro_signal, "recent_signal": recent_signal})
    
    return pd.DataFrame(signal_list)
