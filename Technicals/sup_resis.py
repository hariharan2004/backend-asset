import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from collections import Counter

def load_data(file_path, num_rows=200):
    data = pd.read_csv(file_path)
    data = data.head(num_rows)
    data['Start'] = pd.to_datetime(data['Start'], errors='coerce')
    data['End'] = pd.to_datetime(data['End'], errors='coerce')
    data.dropna(subset=['Start', 'End'], inplace=True)
    data.sort_values(by='Start', inplace=True)
    return data

def process_data(data, eps=100, min_samples=5, max_diff=500, close_threshold=100):
    prices = pd.concat([data['Close'], data['High'], data['Low'], data['Open']])
    prices = prices.values.reshape(-1, 1)

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    clusters = dbscan.fit_predict(prices)

    range_levels = []
    cluster_counter = Counter(clusters)

    for cluster in set(clusters):
        if cluster == -1:
            continue
        cluster_prices = prices[clusters == cluster]
        min_price = cluster_prices.min()
        max_price = cluster_prices.max()
        density = cluster_counter[cluster]
        if max_price - min_price <= max_diff:
            range_levels.append((min_price, max_price, density))

    merged_levels = merge_ranges(range_levels, max_diff, close_threshold)
    return merged_levels

def merge_ranges(ranges, max_diff=500, close_threshold=100):
    if not ranges:
        return ranges

    ranges.sort()
    merged_ranges = [ranges[0]]

    for current in ranges[1:]:
        last = merged_ranges[-1]
        if current[0] <= last[1] + close_threshold:
            merged_ranges[-1] = (last[0], max(current[1], last[1]), last[2] + current[2])
        else:
            merged_ranges.append(current)

    final_ranges = []
    for r in merged_ranges:
        if r[1] - r[0] <= max_diff:
            final_ranges.append(r)
        else:
            steps = int((r[1] - r[0]) // max_diff + 1)
            step_size = (r[1] - r[0]) / steps
            for i in range(steps):
                final_ranges.append((r[0] + i * step_size, min(r[0] + (i + 1) * step_size, r[1]), r[2] // steps))

    return final_ranges

def calculate_lower_range_levels(prices, lower_limit, upper_limit, existing_levels, eps=100, min_samples=8):
    filtered_prices = prices[(prices >= lower_limit) & (prices <= upper_limit)]

    # Exclude prices that fall within existing levels
    for low, high, _ in existing_levels:
        filtered_prices = filtered_prices[(filtered_prices < low) | (filtered_prices > high)]

    if len(filtered_prices) == 0:
        return []

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    clusters = dbscan.fit_predict(filtered_prices.reshape(-1, 1))

    range_levels = []
    cluster_counter = Counter(clusters)

    for cluster in set(clusters):
        if cluster == -1:
            continue
        cluster_prices = filtered_prices[clusters == cluster]
        min_price = cluster_prices.min()
        max_price = cluster_prices.max()
        density = cluster_counter[cluster]
        if max_price - min_price <= 500:
            range_levels.append((min_price, max_price, density))

    range_levels.sort(key=lambda x: x[2], reverse=True)
    merged_levels = merge_ranges(range_levels, max_diff=500, close_threshold=100)
    return merged_levels

def plot_levels(data, top_levels, lower_range_levels):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Start'], data['Close'], label='Close Price', color='blue', alpha=0.5)
    plt.plot(data['Start'], data['High'], label='High Price', color='green', alpha=0.5)
    plt.plot(data['Start'], data['Low'], label='Low Price', color='red', alpha=0.5)

    for low, high, _ in top_levels:
        plt.axhline(y=low, color='green', linestyle='--', alpha=0.5)
        plt.axhline(y=high, color='red', linestyle='--', alpha=0.5)
        plt.fill_between(data['Start'], low, high, color='gray', alpha=0.2)

    for low, high, _ in lower_range_levels:
        plt.axhline(y=low, color='purple', linestyle='--', alpha=0.5)
        plt.axhline(y=high, color='orange', linestyle='--', alpha=0.5)
        plt.fill_between(data['Start'], low, high, color='yellow', alpha=0.2)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('BTC Price with Support and Resistance Ranges')
    plt.legend()
    plt.show()

def combine_close_ranges(ranges, close_threshold=100):
    """Combine ranges that are close to each other."""
    if not ranges:
        return []

    ranges.sort()
    combined_ranges = [ranges[0]]

    for current in ranges[1:]:
        last = combined_ranges[-1]
        if current[0] <= last[1] + close_threshold:
            combined_ranges[-1] = (last[0], max(last[1], current[1]), last[2] + current[2])
        else:
            combined_ranges.append(current)

    return combined_ranges

def main(file_path):
    data = load_data(file_path)
    prices = pd.concat([data['Close'], data['High'], data['Low'], data['Open']])
    merged_levels = process_data(data)

    merged_levels.sort(key=lambda x: x[2], reverse=True)
    top_levels = merged_levels[:6]

    # Combine closely situated top levels
    combined_top_levels = combine_close_ranges(top_levels, close_threshold=300)  # Increase threshold as needed

    min_price = prices.min()
    lowest_support_level = min(combined_top_levels, key=lambda x: x[0])[1]
    lower_range_levels = calculate_lower_range_levels(prices.values, min_price, lowest_support_level, combined_top_levels)

    # Combine closely situated lower range levels
    combined_lower_range_levels = combine_close_ranges(lower_range_levels, close_threshold=300)  # Increase threshold as needed

    print("Detected Support and Resistance Ranges:")
    for low, high, density in combined_top_levels:
        print(f"Range: {low:.2f} - {high:.2f} with density {density}")

    print("\nDetected Lower Range Support and Resistance Ranges:")
    for low, high, density in combined_lower_range_levels:
        print(f"Range: {low:.2f} - {high:.2f} with density {density}")

    plot_levels(data, combined_top_levels, combined_lower_range_levels)

if __name__ == "__main__":
    file_path = '/home/hariharan/Crypt/BTC_DAILY/Bitcoin_Historical_Data_Daily.csv'
    main(file_path)
