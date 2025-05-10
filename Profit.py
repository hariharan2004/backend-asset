from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network
from typing import List
import asyncio

app = FastAPI()

# Allow React frontend (adjust origin as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace "*" with your React app URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CURRENT_PRICE = 22.0


def fetch_users_from_mongo(vault_name: str):
    client = MongoClient("mongodb+srv://hari2004haran:Hari2004@cluster0.s1sp5.mongodb.net/")
    db = client["VaultDB"]
    collection = db["transactions"]

    users = {}

    for doc in collection.find():
        wallet = doc["walletAddress"]
        for tx in doc["transactions"]:
            if tx["vaultName"] != vault_name:
                continue
            if wallet not in users:
                users[wallet] = {
                    "deposit": 0.0,
                    "deposit_date": None,
                    "remaining_cash": 0.0,
                    "token_balance": 0.0,
                    "profit": 0.0,
                    "actual_invested": 0.0
                }
            if tx["type"] == "deposit":
                users[wallet]["deposit"] += tx["amount"]
                users[wallet]["remaining_cash"] += tx["amount"]
                if users[wallet]["deposit_date"] is None or tx["date"] < users[wallet]["deposit_date"]:
                    users[wallet]["deposit_date"] = tx["date"]
            elif tx["type"] == "withdraw":
                users[wallet]["deposit"] -= tx["amount"]
                users[wallet]["remaining_cash"] -= tx["amount"]

    return users


async def fetch_trades(subaccount_id):
    network = Network.testnet()
    client = AsyncClient(network)
    response = await client.fetch_spot_subaccount_trades_list(subaccount_id=subaccount_id)
    print("----------------------------------------------------------------")
    print("Response",response)
    print("----------------------------------------------------------------")
    trades = response.get("trades", [])
    print("Trades",trades)
    print("----------------------------------------------------------------")
    trade_list = []
    for trade in trades:
        price = float(trade["price"]["price"]) * 1e12
        quantity = float(trade["price"]["quantity"]) / 1e18
        timestamp = int(trade["executedAt"]) / 1000
        
        trade_list.append({
            "tradeId": trade["tradeId"],
            "marketId": trade["marketId"],  # important addition
            "direction": trade["tradeDirection"].lower(),
            "price": price,
            "quantity": quantity,
            "timestamp": datetime.fromtimestamp(timestamp),
        })
    return trade_list


def process_trades(users, trades):
    for trade in trades:
        trade_date = trade["timestamp"]
        price = trade["price"]
        quantity = trade["quantity"]

        if trade["direction"] == "buy":
            eligible_users = {w: u for w, u in users.items() if u["deposit_date"] is not None and trade_date >= u["deposit_date"]}
            total_cash = sum(u["remaining_cash"] for u in eligible_users.values())
            if total_cash == 0:
                continue

            total_cost = price * quantity

            for user in eligible_users.values():
                user_share = user["remaining_cash"] / total_cash
                user_cost = min(user["remaining_cash"], user_share * total_cost)
                user_qty = user_cost / price

                user["remaining_cash"] -= user_cost
                user["token_balance"] += user_qty
                user["actual_invested"] += user_cost

        elif trade["direction"] == "sell":
            eligible_users = {w: u for w, u in users.items() if u["token_balance"] > 0}
            total_tokens = sum(u["token_balance"] for u in eligible_users.values())
            if total_tokens == 0:
                continue

            for user in eligible_users.values():
                user_share = user["token_balance"] / total_tokens
                user_tokens_to_sell = quantity * user_share
                user_proceeds = user_tokens_to_sell * price

                user["token_balance"] -= user_tokens_to_sell
                user["remaining_cash"] += user_proceeds
                user["profit"] += user_proceeds

    return users

   
def display_dashboard(users):
    dashboard = []
    for wallet, user in users.items():
        token_value = user["token_balance"] * CURRENT_PRICE
        current_value = user["remaining_cash"] + token_value
        profit = current_value - user["deposit"]
        roi = (profit / user["deposit"]) * 100 if user["deposit"] > 0 else 0

        dashboard.append({
            "wallet": wallet,
            "deposit": round(user["deposit"], 2),
            "actual_invested": round(user["actual_invested"], 2),
            "token_value": round(token_value, 2),
            "current_value": round(current_value, 2),
            "token_balance": round(user["token_balance"], 4),
            "remaining_cash": round(user["remaining_cash"], 2),
            "profit": round(profit, 2),
            "roi": round(roi, 2)
        })
    return dashboard


@app.get("/dashboard")
async def get_dashboard(vaults: List[str] = Query(default=["btcusdt", "ethusdt", "injusdt"])):
    results = []

    for vault in vaults:
        users = fetch_users_from_mongo(vault)
        
        # Use a vault-specific subaccount ID (or filter from all trades if you only have one subaccount)
        # For now, we assume you only have 1 subaccount and filter trades by vault
        all_trades = await fetch_trades("0x4a93d364fbf07e57883e5e42bdca9d9e7918e5a5000000000000000000000001")
        
        # Filter trades based on marketId / vaultName if available in the trade
        vault_trades = [t for t in all_trades if vault in t.get("market_id", vault)]  # Add proper filtering here

        updated_users = process_trades(users, vault_trades)
        dashboard = display_dashboard(updated_users)
        results.append({
            "vault": vault,
            "dashboard": dashboard,
        })
    results.append({
            "trade_list":all_trades
    })
    return {"results": results}

