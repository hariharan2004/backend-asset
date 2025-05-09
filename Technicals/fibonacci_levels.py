def find_macro_high_low(data):
    macro_high = None
    macro_low = None
    low_found_after_high = False
    recent_high_index=0
    for i in range(len(data)):
        if macro_high is None or data['High'].iloc[i] > macro_high:
            macro_high = data['High'].iloc[i]
            macro_low = None  # Reset recent low when a new high is found
            recent_high_index=data["Start"].iloc[i]
            low_found_after_high = False
    filtered_data = data[data['Start'] > recent_high_index]
    for i in range(len(filtered_data)):
        if macro_high is not None and (macro_low is None or filtered_data['Low'].iloc[i] < macro_low):
            macro_low = filtered_data['Low'].iloc[i]
            low_found_after_high = True
    print("Index is :",recent_high_index)
    if not low_found_after_high:
        macro_low = filtered_data['Low'].min()
    
    return macro_high, macro_low

def find_recent_high_low(data):
    recent_high=None
    recent_low=None
    low_found_after_high = False
    for i in range(len(data)):
        if recent_high is None or data['High'].iloc[i] > recent_high:
            recent_high=data["High"].iloc[i]
            recent_low=None
            low_found_after_high = False
        if recent_high is not None and (recent_low is None or data['Low'].iloc[i] < recent_low):
            recent_low = data['Low'].iloc[i]
            low_found_after_high = True
    if not low_found_after_high:
        recent_low = data['Low'].min()
    return recent_high, recent_low


def calculate_fibonacci(data):

    last_200_days = data.head(200).reset_index(drop=True)
    last_50_days=data.head(50).reset_index(drop=True)

    macro_high_price,macro_low_price = find_macro_high_low(last_200_days)
    recent_high_price,recent_low_price = find_recent_high_low(last_50_days)
    fib_levels = [0, 0.236, 0.25, 0.5, 0.75, 0.786, 1]
    macro_fib_prices = {level: macro_high_price - (macro_high_price - macro_low_price) * level for level in fib_levels}
    recent_fib_prices = {level: recent_high_price - (recent_high_price - recent_low_price) * level for level in fib_levels}
    
    return macro_fib_prices,recent_fib_prices
#print("----------------------")