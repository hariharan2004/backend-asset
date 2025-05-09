import pandas as pd
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

    current_btc_price_low = current_btc_price
    current_btc_price_high = current_btc_price
    current_btc_price_low = min(current_btc_price_low, current_btc_price)
    current_btc_price_high = max(current_btc_price_high, current_btc_price)
    
    previous_btc_price_close = data['Close'].iloc[-1]
    closing_time = "00:20:00"
    
    data['Start'] = pd.to_datetime(data['Start'])
    data = data.sort_values(by='Start')
    data = calculate_ma(data)
    
    ma200 = data["200-Day MA"].iloc[-1]
    ma100 = data["100-Day MA"].iloc[-1]
    ma50 = data["50-Day MA"].iloc[-1]
    
    print("200 D MA:", ma200)
    print("100 D MA:", ma100)
    print("50 D MA:", ma50)
    print("Previous Closing Price:", previous_btc_price_close)
    
    if ma50 > ma100 > ma200:
        if current_btc_price < ma200 and current_btc_price > ma100 and current_btc_price > ma50 and current_btc_price>=ma200-ma200*0.05:
            if previous_btc_price_close < ma200:
                signal.loc[0, 'Moving Average'] = "SELL-MA200-1"
            elif previous_btc_price_close > ma200:
                if current_btc_price < ma200 and closing_time < "00:00:10":
                    signal.loc[0, 'Moving Average'] = "SELL-MA200-2"
                elif current_btc_price_high > ma200 and current_btc_price < ma200 - ma200 * 0.01:
                    if current_btc_price < ma200 and closing_time < "00:00:10":
                        signal.loc[0, 'Moving Average'] = "SELL-MA200-3"
                    else:
                        signal.loc[0, 'Moving Average'] = "BUY-200"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA200-4"
            else:
                if current_btc_price > ma200 + ma200 * 0.01 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "BUY-MA200-5"
                elif current_btc_price < ma200 - ma200 * 0.01 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "SELL-MA200-6"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA200-7"
        elif current_btc_price < ma100 and current_btc_price > ma200 and current_btc_price>=ma100-ma100*0.05:
            if previous_btc_price_close < ma100:
                signal.loc[0, 'Moving Average'] = "SELL-MA100"
            elif previous_btc_price_close > ma100:
                if current_btc_price < ma100 and closing_time < "00:00:10":
                    signal.loc[0, 'Moving Average'] = "SELL-MA100"
                elif current_btc_price_high > ma100 and current_btc_price < ma100 - ma100 * 0.01:
                    if current_btc_price < ma100 and closing_time < "00:00:10":
                        signal.loc[0, 'Moving Average'] = "SELL-MA100"
                    else:
                        signal.loc[0, 'Moving Average'] = "BUY-MA100"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA100"
            else:
                if current_btc_price > ma100 + ma100 * 0.01 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "BUY-MA100"
                elif current_btc_price < ma100 - ma100 * 0.01 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "SELL-MA100"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA100"
        elif current_btc_price < ma50 and current_btc_price > ma100 and current_btc_price>=ma50-ma50*0.05:
            if previous_btc_price_close < ma50:
                signal.loc[0, 'Moving Average'] = "SELL-MA50"
            elif previous_btc_price_close > ma50:
                if current_btc_price < ma50 and closing_time < "00:00:10":
                    signal.loc[0, 'Moving Average'] = "SELL-MA50"
                elif current_btc_price_high > ma50 and current_btc_price < ma50 - ma50 * 0.01:
                    if current_btc_price < ma50 and closing_time < "00:00:10":
                        signal.loc[0, 'Moving Average'] = "SELL-MA50"
                    else:
                        signal.loc[0, 'Moving Average'] = "BUY-MA50-1"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA50"
            else:
                if current_btc_price > ma50 + ma50 * 0.01 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "BUY-MA50-2"
                elif current_btc_price < ma50 - ma50 * 0.01 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "SELL-MA50"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA50"
        elif current_btc_price > ma200 and current_btc_price < ma100 and current_btc_price < ma50 and current_btc_price <= ma200 + (ma200 * 0.05): # changed
            if previous_btc_price_close > ma200:
                if current_btc_price < ma200 - ma200 * 0.01 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "SELL-MA200-8"
                elif current_btc_price > ma200 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "BUY-MA200-9"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA200-10"
            elif previous_btc_price_close < ma200:
                if current_btc_price > ma200 + ma200 * 0.01:
                    signal.loc[0, 'Moving Average'] = "BUY-MA200-11"
                elif current_btc_price < ma200 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "SELL-MA200-12"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA200-13"
            else:
                signal.loc[0, 'Moving Average'] = "NEUTRAL-MA200-14"
        elif current_btc_price > ma100 and current_btc_price < ma50 and current_btc_price <= ma100 + (ma100 * 0.05):
            if previous_btc_price_close > ma100:
                if current_btc_price < ma100 - ma100 * 0.01 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "SELL-MA100"
                elif current_btc_price > ma100 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "BUY-MA100"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA100"
            elif previous_btc_price_close < ma100:
                if current_btc_price > ma100 + ma100 * 0.01:
                    signal.loc[0, 'Moving Average'] = "BUY-MA100"
                elif current_btc_price < ma100 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "SELL-MA100"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA100"
            else:
                signal.loc[0, 'Moving Average'] = "NEUTRAL-MA100"
        elif current_btc_price > ma50 and current_btc_price <= ma50 + (ma50 * 0.05):
            if previous_btc_price_close > ma50:
                if current_btc_price < ma50 - ma50 * 0.01 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "SELL-MA50"
                elif current_btc_price > ma50 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "BUY-MA50-3"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA50"
            elif previous_btc_price_close < ma50:
                if current_btc_price > ma50 + ma50 * 0.01:
                    signal.loc[0, 'Moving Average'] = "BUY-MA50-4"
                elif current_btc_price < ma50 and closing_time < "00:10:00":
                    signal.loc[0, 'Moving Average'] = "SELL-MA50"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA50"
            else:
                signal.loc[0, 'Moving Average'] = "NEUTRAL-MA50"
    elif ma50<ma100<ma200:
        if current_btc_price<ma50 and current_btc_price>ma50-ma50*0.02:
            if current_btc_price_high>ma50 and current_btc_price<current_btc_price_high-current_btc_price_high*0.005:
                if current_btc_price<ma50:
                    signal.loc[0, 'Moving Average'] = "SELL-MA50"
                elif current_btc_price>ma50 and closing_time<"15min":
                    signal.loc[0, 'Moving Average'] = "BUY-MA50-5"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA50"
            else:
                signal.loc[0, 'Moving Average'] = "NEUTRAL-MA50"
    elif ma50<ma200<ma100 and current_btc_price>ma50-ma50*0.02:
        if current_btc_price>ma100 and current_btc_price<ma100+ma100*0.025:
            if current_btc_price_low>ma100-ma100*0.01:
                signal.loc[0, 'Moving Average'] = "BUY-MA100"
            elif current_btc_price<ma100 and closing_time<"00:10:00":
                signal.loc[0, 'Moving Average'] = "SELL-MA100"
            else:
                signal.loc[0, 'Moving Average'] = "NEUTRAL-MA50"
        if current_btc_price<ma200 and previous_btc_price_close>ma50 and current_btc_price_low>ma50-ma50*0.02:
            if current_btc_price>ma50:
                signal.loc[0, 'Moving Average'] = "BUY-MA50-6"
            else:
                signal.loc[0, 'Moving Average'] = "NEUTRAL-MA50"
        elif current_btc_price<ma200 and previous_btc_price_close<ma50:
            if current_btc_price<ma50:
                signal.loc[0, 'Moving Average'] = "SELL-MA50"
            elif current_btc_price>ma50:
                signal.loc[0, 'Moving Average'] = "BUY-MA50-7"
            else:
                signal.loc[0, 'Moving Average'] = "NEUTRAL-MA50"
        elif current_btc_price>ma50:
            if current_btc_price<ma200-ma200*0.01:
                if previous_btc_price_close>ma200:
                    if current_btc_price_low>ma200-ma200*0.015 and current_btc_price>ma50:
                        if current_btc_price>ma200:
                            signal.loc[0, 'Moving Average'] = "BUY-MA200-15"
                        else:
                            signal.loc[0, 'Moving Average'] = "SELL-MA200-16"
                    else:
                        signal.loc[0, 'Moving Average'] = "NEUTRAL-MA200-17"
                elif previous_btc_price_close<ma200:
                    if current_btc_price_low>ma200-ma200*0.015 and current_btc_price>ma50:
                        if current_btc_price>ma200:
                            signal.loc[0, 'Moving Average'] = "BUY-MA200-18"
                        else:
                            signal.loc[0, 'Moving Average'] = "SELL-MA200-19"
                    else:
                        signal.loc[0, 'Moving Average'] = "NEUTRAL-MA200-20"
                else:
                    if current_btc_price_low>ma200-ma200*0.015 and current_btc_price>ma50:
                        if current_btc_price>ma200:
                            signal.loc[0, 'Moving Average'] = "BUY-MA200-21"
                        else:
                            signal.loc[0, 'Moving Average'] = "SELL-MA200-22"
                    else:
                        signal.loc[0, 'Moving Average'] = "NEUTRAL-MA200-23"
            elif current_btc_price>ma200:
                if previous_btc_price_close>ma200 and current_btc_price>ma200:
                    if current_btc_price_low>ma200-ma200*0.01:
                        signal.loc[0, 'Moving Average'] = "BUY-MA200-24"
                    else:
                        signal.loc[0, 'Moving Average'] = "SELL-MA200-25"
                elif previous_btc_price_close<ma200 and current_btc_price>ma200:
                    if current_btc_price_low>ma200-ma200*0.01:
                        signal.loc[0, 'Moving Average'] = "BUY-MA200-26"
                    else:
                        signal.loc[0, 'Moving Average'] = "SELL-MA200-27"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA200-28"
            else:
                signal.loc[0, 'Moving Average'] = "NEUTRAL-MA200-29"
        elif current_btc_price>ma200:
            if current_btc_price_high>ma100:
                if current_btc_price<ma100 and closing_time<"00:10:00":
                    signal.loc[0, 'Moving Average'] = "SELL-MA100"
                elif current_btc_price>ma100 and current_btc_price_low>ma100-ma100*0.01:
                    signal.loc[0, 'Moving Average'] = "BUY-MA100"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA100"
            elif current_btc_price_low>ma100-ma100*0.01:
                if current_btc_price<ma100 and closing_time<"00:10:00":
                    signal.loc[0, 'Moving Average'] = "SELL-MA100"
                elif current_btc_price>ma100:
                    signal.loc[0, 'Moving Average'] = "BUY-MA100"
                else:
                    signal.loc[0, 'Moving Average'] = "NEUTRAL-MA100"
        else:
            signal.loc[0, 'Moving Average'] = "NEUTRAL-else"
    else:
        signal.loc[0, 'Moving Average'] = "NEUTRAL"
    
    return signal
