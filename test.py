import asyncio
import time
from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network

async def fetch_oracle_prices(client):
    try:
        markets = await client.all_derivative_markets()
        if not markets:
            print("No markets found.")
            return

        market_address = "0x4ca0f92fc28be0c9761326016b5a1a2177dd6375558365116b5bdda9abc229ce"
        market = markets.get(market_address)

        if not market:
            print(f"Market not found for address: {market_address}")
            return

        base_symbol = market.oracle_base
        quote_symbol = market.oracle_quote
        oracle_type = market.oracle_type

        oracle_prices = await client.fetch_oracle_price(
            base_symbol=base_symbol,
            quote_symbol=quote_symbol,
            oracle_type=oracle_type,
        )

        # Extract the actual price from the oracle_prices dictionary
        current_price = float(oracle_prices['price'])

        # Initialize min and max prices if not already set
        global current_price_low, current_price_high
        if current_price_low is None:
            current_price_low = current_price
        if current_price_high is None:
            current_price_high = current_price

        # Update min and max prices based on current price
        current_price_low = min(current_price_low, current_price)
        current_price_high = max(current_price_high, current_price)
        print("--------------------------------------------------")
        print(f"BTC PRICE: {current_price}")
        print(f"BTC HIGH PRICE: {current_price_high}")
        print(f"BTC LOW PRICE: {current_price_low}")
        print("--------------------------------------------------")
    except Exception as e:
        print(f"Error fetching oracle prices: {e}")

async def main():
    global current_price_low, current_price_high
    current_price_low = None
    current_price_high = None

    network = Network.mainnet()  # Switch to mainnet for production
    client = AsyncClient(network)

    while True:
        await fetch_oracle_prices(client)
        await asyncio.sleep(10)  # Fetch prices every 10 seconds

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"Unhandled exception: {e}")
            print("Retrying in 60 seconds...")
            time.sleep(10)  # Wait before retrying
