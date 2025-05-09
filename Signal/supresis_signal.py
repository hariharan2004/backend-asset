import pandas as pd
from Utils.utils import get_current_price
from Technicals.sup_resis import load_data, process_data, calculate_lower_range_levels

async def supresiss_signal(data_path):
    signal = pd.DataFrame(columns=["Sup Resis"])
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

    current_price_low = current_btc_price
    current_price_high = current_btc_price
    current_price_low = min(current_price_low, current_btc_price)
    current_price_high = max(current_price_high, current_btc_price)
    
    prev_close = data['Close'].iloc[1]
    closing_time = "00:15:00"
    
    print("Current BTC Price:", current_btc_price)
    data = load_data(data_path)
    prices = pd.concat([data['Close'], data['High'], data['Low'], data['Open']])
    merged_levels = process_data(data)
    
    # Sort and select top levels
    merged_levels.sort(key=lambda x: x[2], reverse=True)
    top_levels = merged_levels[:6]

    # Calculate the minimum price from the prices
    min_price = prices.min()
    
    # Calculate the lowest support level from the top levels
    lowest_support_level = min(top_levels, key=lambda x: x[0])[1]
    
    # Automatically calculate the lower range levels
    lower_range_levels = calculate_lower_range_levels(prices.values, min_price, lowest_support_level, top_levels)
    
    # Print detected ranges
    print("Detected Support and Resistance Ranges:")
    for low, high, density in top_levels:
        print(f"Range: {low:.2f} - {high:.2f} with density {density}")

    print("\nDetected Lower Range Support and Resistance Ranges:")
    for low, high, density in lower_range_levels:
        print(f"Range: {low:.2f} - {high:.2f} with density {density}")

    # Combine all levels for easier comparison
    all_levels = top_levels + lower_range_levels
    
    # Find the closest lower range
    closest_lower = max((level for level in all_levels if level[1] < current_btc_price), key=lambda x: x[1], default=None)
    
    # Find the closest upper range
    closest_upper = min((level for level in all_levels if level[0] > current_btc_price), key=lambda x: x[0], default=None)
    
    # Previous ranges
    prev_below = 61400
    prev_above = 62450
    
    # Define initial above and below levels
    above = closest_upper[0] if closest_upper else float('inf')  # Set a high default value
    below = closest_lower[1] if closest_lower else float('-inf')  # Set a low default value


    # Print the closest lower and upper ranges
    print("\nClosest Ranges to Current BTC Price:")
    if closest_lower:
        print(f"Closest Lower Range: {closest_lower[0]:.2f} - {closest_lower[1]:.2f} with density {closest_lower[2]}")
    else:
        print("No lower range found.")
    
    if closest_upper:
        print(f"Closest Upper Range: {closest_upper[0]:.2f} - {closest_upper[1]:.2f} with density {closest_upper[2]}")
    else:
        print("No upper range found.")
    
    # Signal generation logic
    if current_btc_price < below:
        prev_above = above
        prev_below = below
        above = below
        below = closest_lower[1] if closest_lower else None
        
    elif current_btc_price > above:
        prev_below = above
        prev_above = below
        below = above
        above = closest_upper[0] if closest_upper else None
    
    if prev_close > below:
        if current_btc_price > below:
            if closing_time == "00:15:00" or current_price_low > below - 0.01 * below: # <
                signal.loc[len(signal)] = ["buy-1"]
            elif current_price_low > below - 0.01 * below:
                signal.loc[len(signal)] = ["buy-1"]
            else:
                signal.loc[len(signal)] = ["neutral-1"]
        elif current_btc_price < below:
            if closing_time == "00:15:00" or current_price_low < below - 0.01 * below: # <
                signal.loc[len(signal)] = ["sell-2"]
            else:
                signal.loc[len(signal)] = ["neutral-2"]
    elif prev_close < below:
        if current_btc_price < prev_below and current_price_high in range(int(prev_below), int(prev_above)):
            if current_btc_price > below + 0.01 * below:
                signal.loc[len(signal)] = ["buy-3"]
            elif current_btc_price > below and closing_time == "00:15:00": # <
                signal.loc[len(signal)] = ["buy-3"]
            elif current_btc_price < below and closing_time == "00:15:00": # <
                signal.loc[len(signal)] = ["sell-3"]
            elif current_btc_price < prev_below - 0.01 * prev_below:
                signal.loc[len(signal)] = ["sell-3"]
            else:
                signal.loc[len(signal)] = ["neutral-3"]
    elif current_btc_price > prev_below:
        if current_btc_price > below + 0.01 * below:
            signal.loc[len(signal)] = ["buy-4"]
        elif current_btc_price < prev_below and current_price_high > prev_below - 0.005 * prev_below:
            if current_btc_price < prev_below - 0.01 * prev_below:
                signal.loc[len(signal)] = ["sell-4"]
            elif closing_time == "00:15:00" and current_btc_price < below - 0.005 * below: # <
                signal.loc[len(signal)] = ["sell-4"]
            else:
                signal.loc[len(signal)] = ["neutral-4"]
    else:
        signal.loc[len(signal)] = ["neutral-default"]

    return signal
