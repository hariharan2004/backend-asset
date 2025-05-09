import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import ma
import bollinger_bands
import fibonacci_levels

def plot_btc_price(data):
    data['Start'] = pd.to_datetime(data['Start'])
    data = data.sort_values(by='Start')
    
    # Calculate moving averages and Bollinger Bands
    ma_data = ma.calculate_ma(data)
    data = bollinger_bands.calculate_bollinger_bands(data)
    
    last_30_days = data.tail(30).reset_index(drop=True)
    last_100_days = data.tail(100).reset_index(drop=True)
    
    # Calculate Fibonacci levels
    fib_prices_macro, fib_prices_recent = fibonacci_levels.calculate_fibonacci(last_100_days)
    
    # Print Moving Averages for reference
    print(f"50-Day Moving Average: {ma_data['50-Day MA'].dropna().iloc[-1]}")
    print(f"100-Day Moving Average: {ma_data['100-Day MA'].dropna().iloc[-1]}")
    print(f"200-Day Moving Average: {ma_data['200-Day MA'].dropna().iloc[-1]}")

    # Plot the data
    plt.figure(figsize=(14, 7))
    plt.plot(last_30_days['Start'], last_30_days['Close'], label='Closing Price', marker='o')
    plt.plot(last_30_days['Start'], last_30_days['High'], label='High Price', alpha=0.3)
    plt.plot(last_30_days['Start'], last_30_days['Low'], label='Low Price', alpha=0.3)
    plt.plot(last_30_days['Start'], data['50-Day MA'].tail(30), label='50-Day MA', color='black', linewidth=2)
    plt.plot(last_30_days['Start'], data['100-Day MA'].tail(30), label='100-Day MA', color='blue', linewidth=2)
    plt.plot(last_30_days['Start'], data['200-Day MA'].tail(30), label='200-Day MA', color='blue', linewidth=2)
    plt.plot(last_30_days['Start'], data['Middle Band'].tail(30), label='Middle Band', color='purple', linewidth=2)
    plt.plot(last_30_days['Start'], data['Upper Band'].tail(30), label='Upper Band', color='green', linewidth=2)
    plt.plot(last_30_days['Start'], data['Lower Band'].tail(30), label='Lower Band', color='red', linewidth=2)

    # Plot Fibonacci levels (macro and recent)
    for level, price in fib_prices_macro.items():
        plt.axhline(price, color='black', linestyle='--', linewidth=1)
        plt.text(last_100_days['Start'].iloc[-1], price, f'{level*100:.1f}% ({price:.2f})', verticalalignment='bottom')
    
    for level, price in fib_prices_recent.items():
        plt.axhline(price, color='black', linestyle='--', linewidth=1)
        plt.text(last_100_days['Start'].iloc[-1], price, f'{level*100:.1f}% ({price:.2f})', verticalalignment='bottom')

    # Adjust y-axis limits to accommodate both the Bollinger Bands and Fibonacci levels
    min_price = min(data['Low'].tail(30).min(), data['Lower Band'].tail(30).min(),
                    min(fib_prices_macro.values()), min(fib_prices_recent.values()))
    max_price = max(data['High'].tail(30).max(), data['Upper Band'].tail(30).max(),
                    max(fib_prices_macro.values()), max(fib_prices_recent.values()))

    plt.ylim(min_price * 0.95, max_price * 1.05)
    
    # Add labels, title, legend, and grid
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('BTC Price Action with Bollinger Bands and Fibonacci Levels')
    plt.legend()
    plt.grid(True)

    # Save the plot
    output_dir = '/home/hariharan/Crypt/BTC_DAILY/Plots'
    os.makedirs(output_dir, exist_ok=True)
    filename = datetime.now().strftime('BTC_Price_Plot_%Y%m%d.png')
    plt.savefig(os.path.join(output_dir, filename))
    
    # Display the plot
    plt.show()

if __name__ == "__main__":
    data = pd.read_csv('/home/hariharan/Crypt/BTC_DAILY/Bitcoin_Historical_Data_Daily.csv')
    data = data.head(200)  # Using the most recent 200 data points
    plot_btc_price(data)
