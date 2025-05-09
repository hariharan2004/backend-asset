import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from collections import Counter

# Load BTC historical data
file_path = '/home/hariharan/Crypt/BTC_DAILY/Bitcoin_Historical_Data_Daily.csv'
data = pd.read_csv(file_path)
data = data.head(100)
data['Start'] = pd.to_datetime(data['Start'], errors='coerce')
data['End'] = pd.to_datetime(data['End'], errors='coerce')
data.dropna(subset=['Start', 'End'], inplace=True)
data.sort_values(by='Start', inplace=True)

# Combine close, high, low, and open prices into a single array for clustering
prices = pd.concat([data['Close'], data['High'], data['Low'], data['Open']])
prices = prices.values.reshape(-1, 1)

# Use DBSCAN for clustering
dbscan = DBSCAN(eps=100, min_samples=5)  # Adjust eps value for finer clustering
clusters = dbscan.fit_predict(prices)

# Identify support and resistance ranges with density hits
range_levels = []
cluster_counter = Counter(clusters)

for cluster in set(clusters):
    if cluster == -1:
        continue
    cluster_prices = prices[clusters == cluster]
    min_price = cluster_prices.min()
    max_price = cluster_prices.max()
    density = cluster_counter[cluster]
    if max_price - min_price <= 500:
        range_levels.append((min_price, max_price, density))

# Merge overlapping or closely situated ranges
def merge_ranges(ranges, max_diff=500, close_threshold=100):
    if not ranges:
        return ranges

    # Sort ranges by their start value
    ranges.sort()
    merged_ranges = [ranges[0]]

    for current in ranges[1:]:
        last = merged_ranges[-1]
        if current[0] <= last[1] + close_threshold:  # Check for overlap or close proximity
            # Merge ranges even if combined range exceeds 500, if they are close
            merged_ranges[-1] = (last[0], max(current[1], last[1]), last[2] + current[2])
        else:
            merged_ranges.append(current)

    # Ensure all ranges are within the max_diff constraint after merging
    final_ranges = []
    for r in merged_ranges:
        if r[1] - r[0] <= max_diff:
            final_ranges.append(r)
        else:
            # If a range exceeds max_diff, split it
            steps = int((r[1] - r[0]) // max_diff + 1)
            step_size = (r[1] - r[0]) / steps
            for i in range(steps):
                final_ranges.append((r[0] + i * step_size, min(r[0] + (i + 1) * step_size, r[1]), r[2] // steps))

    return final_ranges

# Function to calculate lower range levels
def calculate_lower_range_levels(prices, lower_limit, upper_limit, eps=100, min_samples=5):
    # Filter prices within the specified range
    filtered_prices = prices[(prices >= lower_limit) & (prices <= upper_limit)]
    
    if len(filtered_prices) == 0:
        return []

    # Use DBSCAN for clustering
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
    merged_levels = merge_ranges(range_levels)
    return merged_levels

# Calculate levels for the lower range (50,000 to 58,230)
lower_range_levels = calculate_lower_range_levels(prices.flatten(), 50000, 58230)

# Sort levels by density and select top levels
range_levels.sort(key=lambda x: x[2], reverse=True)
merged_levels = merge_ranges(range_levels)

# Select top 6 merged levels by density
merged_levels.sort(key=lambda x: x[2], reverse=True)
top_levels = merged_levels[:6]

# Print the identified support and resistance ranges
print("Detected Support and Resistance Ranges:")
for low, high, density in top_levels:
    print(f"Range: {low:.2f} - {high:.2f} with density {density}")

print("\nDetected Lower Range Support and Resistance Ranges:")
for low, high, density in lower_range_levels:
    print(f"Range: {low:.2f} - {high:.2f} with density {density}")

# Plotting the data
plt.figure(figsize=(14, 7))
plt.plot(data['Start'], data['Close'], label='Close Price', color='blue', alpha=0.5)
plt.plot(data['Start'], data['High'], label='High Price', color='green', alpha=0.5)
plt.plot(data['Start'], data['Low'], label='Low Price', color='red', alpha=0.5)

for low, high, _ in top_levels:
    plt.axhline(y=low, color='green', linestyle='--', alpha=0.5)
    plt.axhline(y=high, color='red', linestyle='--', alpha=0.5)
    plt.fill_between(data['Start'], low, high, color='gray', alpha=0.2)

# Plot lower range levels separately
for low, high, _ in lower_range_levels:
    plt.axhline(y=low, color='purple', linestyle='--', alpha=0.5)
    plt.axhline(y=high, color='orange', linestyle='--', alpha=0.5)
    plt.fill_between(data['Start'], low, high, color='yellow', alpha=0.2)

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('BTC Price with Support and Resistance Ranges')
plt.legend()
plt.show()
