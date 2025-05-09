from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network
from Technicals.fetch_btc_price import fetch_oracle_prices
async def get_current_price():
    network = Network.mainnet()  
    client = AsyncClient(network)
    price = await fetch_oracle_prices(client)
    print("Current price is:",price)
    return price

