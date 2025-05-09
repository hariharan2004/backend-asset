import asyncio
import time
import csv
import os
from datetime import datetime, timedelta
from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network
csv_file_path = "btc_prices.csv"
current_price_low = None
current_price_high = None
open_price = None
start_date = datetime.now().strftime("%Y-%m-%d")

async def fetch_oracle_prices(client):
    global current_price_low, current_price_high, open_price, start_date

    if client is None:
        print("Client is not initialized.")
        return None

    try:
        markets = await client.all_derivative_markets()
        if not markets:
            print("No markets found.")
            return None

        market_address = "0x4ca0f92fc28be0c9761326016b5a1a2177dd6375558365116b5bdda9abc229ce"
        market = markets.get(market_address)

        if not market:
            print(f"Market not found for address: {market_address}")
            return None

        base_symbol = market.oracle_base
        quote_symbol = market.oracle_quote
        oracle_type = market.oracle_type

        oracle_prices = await client.fetch_oracle_price(
            base_symbol=base_symbol,
            quote_symbol=quote_symbol,
            oracle_type=oracle_type,
        )
        current_price = float(oracle_prices['price'])
        if open_price is None:
            open_price = current_price
        if current_price_low is None:
            current_price_low = current_price
        if current_price_high is None:
            current_price_high = current_price
        current_price_low = min(current_price_low, current_price)
        current_price_high = max(current_price_high, current_price)
        print(f"BTC PRICE: {current_price}")
        print(f"BTC HIGH PRICE: {current_price_high}")
        print(f"BTC LOW PRICE: {current_price_low}")
        now = datetime.now()
        end_of_day = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
        time_remaining = end_of_day - now
        print(f"Time until end of 24-hour period: {str(time_remaining).split('.')[0]}")
        current_date = datetime.now().strftime("%Y-%m-%d")
        if current_date != start_date:
            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([start_date, current_date, open_price, current_price_high, current_price_low, current_price])
            start_date = current_date
            open_price = current_price
            current_price_low = current_price
            current_price_high = current_price

        return current_price

    except Exception as e:
        print(f"Error fetching oracle prices: {e}")
        return None

async def main():
    network = Network.mainnet()  # Switch to mainnet for production
    client = AsyncClient(network)
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Start", "End", "Open", "High", "Low", "Close"])

    while True:
        await fetch_oracle_prices(client)
        await asyncio.sleep(5)  # Fetch prices every 5 seconds

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"Unhandled exception: {e}")
            print("Retrying in 10 seconds...")
            time.sleep(10)  # Wait before retrying
