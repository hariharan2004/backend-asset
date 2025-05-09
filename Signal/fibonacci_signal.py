from Technicals.fibonacci_levels import calculate_fibonacci
import pandas as pd
from Utils.utils import get_current_price

async def fib_signal(data_path):
    signal_list = [] 
    data = pd.read_csv(data_path)
    
    current_btc_price = await get_current_price()
    
    if current_btc_price is None:
        return pd.DataFrame(columns=["macro_signal", "recent_signal"])
    
    current_btc_price_low = min(data['Low'].min(), current_btc_price)
    current_btc_price_high = max(data['High'].max(), current_btc_price)
    
    macro_fib_level, recent_fib_level = calculate_fibonacci(data)
    '''
    def find_closest_levels(fib_levels, current_price, prev_levels):
        above = {}
        below = {}

        for level, price in fib_levels.items():
            if level not in [0, 1]:  # Skip levels 0 and 1
                if price > current_price:
                    above[level] = price
                elif price < current_price:
                    below[level] = price

        closest_above_level = None
        closest_below_level = None

        if above:
            closest_above_level = min(above, key=above.get)
            if closest_above_level in [0.75, 0.786]:
                above = {0.75: fib_levels.get(0.75), 0.786: fib_levels.get(0.786)}
                prev_levels = {0.75: prev_levels.get(0.75), 0.786: prev_levels.get(0.786)}
            elif closest_above_level in [0.25, 0.236]:
                above = {0.25: fib_levels.get(0.25), 0.236: fib_levels.get(0.236)}
                prev_levels = {0.25: prev_levels.get(0.25), 0.236: prev_levels.get(0.236)}
            else:
                above = {closest_above_level: fib_levels[closest_above_level]}
                prev_levels = {closest_above_level: prev_levels.get(closest_above_level)}

        if below:
            closest_below_level = max(below, key=below.get)
            if closest_below_level in [0.75, 0.786]:
                below = {0.75: fib_levels.get(0.75), 0.786: fib_levels.get(0.786)}
                prev_levels = {0.75: prev_levels.get(0.75), 0.786: prev_levels.get(0.786)}
            elif closest_below_level in [0.25, 0.236]:
                below = {0.25: fib_levels.get(0.25), 0.236: fib_levels.get(0.236)}
                prev_levels = {0.25: prev_levels.get(0.25), 0.236: prev_levels.get(0.236)}
            else:
                below = {closest_below_level: fib_levels[closest_below_level]}
                prev_levels = {closest_below_level: prev_levels.get(closest_below_level)}

        return above, below, prev_levels
    '''
    
    def find_closest_levels(fib_levels, current_price):
        above = {}
        below = {}

        for level, price in fib_levels.items():
            if level not in [0, 1]:  # Skip levels 0 and 1
                if price > current_price:
                    above[level] = price
                elif price < current_price:
                    below[level] = price

        closest_above_level = None
        closest_below_level = None

        if above:
            closest_above_level = min(above, key=above.get)
            if closest_above_level in [0.75, 0.786]:
                above = {0.75: fib_levels.get(0.75), 0.786: fib_levels.get(0.786)}
            elif closest_above_level in [0.25, 0.236]:
                above = {0.25: fib_levels.get(0.25), 0.236: fib_levels.get(0.236)}
            else:
                above = {closest_above_level: fib_levels[closest_above_level]}

        if below:
            closest_below_level = max(below, key=below.get)
            if closest_below_level in [0.75, 0.786]:
                below = {0.75: fib_levels.get(0.75), 0.786: fib_levels.get(0.786)}
            elif closest_below_level in [0.25, 0.236]:
                below = {0.25: fib_levels.get(0.25), 0.236: fib_levels.get(0.236)}
            else:
                below = {closest_below_level: fib_levels[closest_below_level]}

        return above, below
    # macro_above, macro_below, prev_macro_above = find_closest_levels(macro_fib_level, current_btc_price, prev_macro_above)
    # recent_above, recent_below, prev_recent_above = find_closest_levels(recent_fib_level, current_btc_price, prev_recent_above)
    macro_above, macro_below = find_closest_levels(macro_fib_level, current_btc_price)
    recent_above, recent_below= find_closest_levels(recent_fib_level, current_btc_price)

    print("Macro Above:",macro_above)
    print("Macro below:",macro_below)
    print("Recent Above:",recent_above)
    print("Recent Below:",recent_below)
    closing_time = "10min"
    previous_btc_close = 60313
    macro_signal = "Neutral-default"
    
    #prev_macro_above = {level: None for level in [0.5, 0.75, 0.786, 0.25, 0.236]}
    #prev_macro_below = {level: None for level in [0.5, 0.75, 0.786, 0.25, 0.236]}
    #prev_recent_above = {level: None for level in [0.5, 0.75, 0.786, 0.25, 0.236]}
    #prev_recent_below = {level: None for level in [0.5, 0.75, 0.786, 0.25, 0.236]}

    prev_macro_above = {0.5: 61518}
    prev_macro_below = {0.25: 55361, 0.236: 54475}
    prev_recent_above = {0.5: 61818}
    prev_recent_below = {0.25: 57728, 0.236: 57498}
    print(prev_macro_above[0.5])
    # Macro signals 


    #Macro Signals
    if 0.5 in prev_macro_above and current_btc_price > prev_macro_above[0.5]:
        if current_btc_price > macro_below[0.5] and current_btc_price < macro_below[0.5] + macro_below[0.5] * 0.02:
            if previous_btc_close < macro_below[0.5]:
                if current_btc_price > macro_below[0.5] - macro_below[0.5] * 0.01:
                    macro_signal = "BUY-0.5"
                elif current_btc_price < macro_above[0.5] and closing_time < "10min":
                    macro_signal = "SELL-0.5"
                else:
                    macro_signal = "NEUTRAL-0.5"
            elif previous_btc_close > macro_below[0.5]:
                if current_btc_price_low > macro_below[0.5] - macro_below[0.5] * 0.02:
                    if current_btc_price > macro_below[0.5]:
                        macro_signal = "BUY-0.5"
                    elif current_btc_price < macro_below[0.5] and closing_time < "15min":
                        macro_signal = "SELL-0.5"
                    else:
                        macro_signal = "NEUTRAL-0.5"
            else:
                macro_signal = "NEUTRAL-0.5"
    elif 0.75 in prev_macro_above and 0.786 in prev_macro_above and prev_macro_above[0.75] < current_btc_price < prev_macro_above[0.786]:
        if current_btc_price > macro_below[0.75] and current_btc_price < macro_below[0.75] + macro_below[0.75] * 0.02:
            if previous_btc_close < macro_below[0.75]:
                if current_btc_price > macro_below[0.75] - macro_below[0.75] * 0.01:
                    macro_signal = "BUY-0.75"
                elif current_btc_price < macro_below[0.75] and closing_time < "10min":
                    macro_signal = "SELL-0.75"
                else:
                    macro_signal = "NEUTRAL-0.75"
            elif previous_btc_close > macro_below[0.75]:
                if current_btc_price_low > macro_below[0.75] - macro_below[0.75] * 0.02:
                    if current_btc_price > macro_below[0.75]:
                        macro_signal = "BUY-0.75"
                    elif current_btc_price < macro_below[0.75] and closing_time < "15min":
                        macro_signal = "SELL-0.75"
                    else:
                        macro_signal = "NEUTRAL-0.75"
            else:
                macro_signal = "NEUTRAL-0.75"
    elif 0.25 in prev_macro_above and 0.236 in prev_macro_above and prev_macro_above[0.25] < current_btc_price < prev_macro_above[0.236]:
        if current_btc_price > macro_below[0.25] and current_btc_price < macro_below[0.25] + macro_below[0.25] * 0.02:
            if previous_btc_close < macro_below[0.25]:
                if current_btc_price > macro_below[0.25] - macro_below[0.25] * 0.01:
                    macro_signal = "BUY-0.25"
                elif current_btc_price < macro_below[0.25] and closing_time < "10min":
                    macro_signal = "SELL-0.25"
                else:
                    macro_signal = "NEUTRAL-0.25"
            elif previous_btc_close > macro_below[0.25]:
                if current_btc_price_low > macro_below[0.25] - macro_below[0.25] * 0.02:
                    if current_btc_price > macro_below[0.25]:
                        macro_signal = "BUY-0.25"
                    elif current_btc_price < macro_below[0.25] and closing_time < "15min":
                        macro_signal = "SELL-0.25"
                    else:
                        macro_signal = "NEUTRAL-0.25"
            else:
                macro_signal = "NEUTRAL-0.25"

    recent_signal = "Neutral-default"
    
    # Recent signals logic
    if 0.5 in prev_recent_above and current_btc_price > prev_recent_above[0.5]:
        if current_btc_price > recent_below[0.5] and current_btc_price < recent_below[0.5] + recent_below[0.5] * 0.02:
            if previous_btc_close < recent_below[0.5]:
                if current_btc_price > recent_below[0.5] - recent_below[0.5] * 0.01:
                    recent_signal = "BUY-0.5"
                elif current_btc_price < recent_below[0.5] and closing_time < "10min":
                    recent_signal = "SELL-0.5"
                else:
                    recent_signal = "NEUTRAL-0.5"
            elif previous_btc_close > recent_below[0.5]:
                if current_btc_price_low > recent_below[0.5] - recent_below[0.5] * 0.02:
                    if current_btc_price > recent_below[0.5]:
                        recent_signal = "BUY-0.5"
                    elif current_btc_price < recent_below[0.5] and closing_time < "15min":
                        recent_signal = "SELL-0.5"
                    else:
                        recent_signal = "NEUTRAL-0.5"
            else:
                recent_signal = "NEUTRAL-0.5"
    elif 0.75 in prev_recent_above and 0.786 in prev_recent_above and prev_recent_above[0.75] < current_btc_price < prev_recent_above[0.786]:
        if current_btc_price > recent_below[0.75] and current_btc_price < recent_below[0.75] + recent_below[0.75] * 0.02:
            if previous_btc_close < recent_below[0.75]:
                if current_btc_price > recent_below[0.75] - recent_below[0.75] * 0.01:
                    recent_signal = "BUY-0.75"
                elif current_btc_price < recent_below[0.75] and closing_time < "10min":
                    recent_signal = "SELL-0.75"
                else:
                    recent_signal = "NEUTRAL-0.75"
            elif previous_btc_close > recent_below[0.75]:
                if current_btc_price_low > recent_below[0.75] - recent_below[0.75] * 0.02:
                    if current_btc_price > recent_below[0.75]:
                        recent_signal = "BUY-0.75"
                    elif current_btc_price < recent_below[0.75] and closing_time < "15min":
                        recent_signal = "SELL-0.75"
                    else:
                        recent_signal = "NEUTRAL-0.75"
            else:
                recent_signal = "NEUTRAL-0.75"
    elif 0.25 in prev_recent_above and 0.236 in prev_recent_above and prev_recent_above[0.25] < current_btc_price < prev_recent_above[0.236]:
        if current_btc_price > recent_below[0.25] and current_btc_price < recent_below[0.25] + recent_below[0.25] * 0.02:
            if previous_btc_close < recent_below[0.25]:
                if current_btc_price > recent_below[0.25] - recent_below[0.25] * 0.01:
                    recent_signal = "BUY-0.25"
                elif current_btc_price < recent_below[0.25] and closing_time < "10min":
                    recent_signal = "SELL-0.25"
                else:
                    recent_signal = "NEUTRAL-0.25"
            elif previous_btc_close > recent_below[0.25]:
                if current_btc_price_low > recent_below[0.25] - recent_below[0.25] * 0.02:
                    if current_btc_price > recent_below[0.25]:
                        recent_signal = "BUY-0.25"
                    elif current_btc_price < recent_below[0.25] and closing_time < "15min":
                        recent_signal = "SELL-0.25"
                    else:
                        recent_signal = "NEUTRAL-0.25"
            else:
                recent_signal = "NEUTRAL-0.25"

    signal_list.append({"macro_signal": macro_signal, "recent_signal": recent_signal})
    
    signals_df = pd.DataFrame(signal_list)
    return signals_df

