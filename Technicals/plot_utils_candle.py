import pandas as pd
import mplfinance as mpf
from datetime import datetime
data = pd.read_csv('/home/hariharan/Crypt/BTC_DAILY/Bitcoin_Historical_Data_Daily.csv')
data['Start'] = pd.to_datetime(data['Start'])
data = data.sort_values(by='Start')
last_30_days = data.tail(30).reset_index(drop=True)
def find_levels(df):
    levels = []
    for i in range(5, len(df) - 5):
        high_range = df['High'][i-5:i+5]
        low_range = df['Low'][i-5:i+5]
        if df['Low'].iloc[i] == min(low_range):
            levels.append((df['Start'].iloc[i], df['Low'].iloc[i], 'support'))
        if df['High'].iloc[i] == max(high_range):
            levels.append((df['Start'].iloc[i], df['High'].iloc[i], 'resistance'))
    return levels
levels = find_levels(last_30_days)
last_30_days.set_index('Start', inplace=True)
s_r_levels = []

for level in levels:
    if level[2] == 'support':
        s_r_levels.append(mpf.make_addplot([level[1]] * len(last_30_days), color='green', linestyle='--', width=1))
    elif level[2] == 'resistance':
        s_r_levels.append(mpf.make_addplot([level[1]] * len(last_30_days), color='red', linestyle='--', width=1))
mpf.plot(
    last_30_days,
    type='candle',
    style='charles',
    title='BTC Price Action with Support and Resistance Levels',
    ylabel='Price',
    addplot=s_r_levels,
    volume=True,
    figratio=(14, 7),
    figscale=1.2
)
mpf.show()
