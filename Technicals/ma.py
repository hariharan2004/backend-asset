import pandas as pd

def calculate_ma(data):
    data['50-Day MA'] = data['Close'].rolling(window=50).mean()
    data['100-Day MA'] = data['Close'].rolling(window=100).mean()
    data['200-Day MA'] = data['Close'].rolling(window=200).mean()
    
    
    return data