from datetime import datetime

# Constants
CURRENT_PRICE = 22.0  # Simulated current token price
VAULT_NAME = "btcusdt"  # Vault name to filter by


# 1. Simulate user transactions
def fetch_dummy_users():
    users = {
        "wallet_1": {
            "deposit": 1500.0,
            "deposit_date": datetime(2024, 9, 1),
            "remaining_cash": 1500.0,
            "token_balance": 0.0,
            "profit": 0.0,
            "actual_invested": 0.0
        },
        "wallet_2": {
            "deposit": 1000.0,
            "deposit_date": datetime(2024, 9, 2),
            "remaining_cash": 1000.0,
            "token_balance": 0.0,
            "profit": 0.0,
            "actual_invested": 0.0
        },
        "wallet_3": {
            "deposit": 2000.0,
            "deposit_date": datetime(2024, 9, 3),
            "remaining_cash": 2000.0,
            "token_balance": 0.0,
            "profit": 0.0,
            "actual_invested": 0.0
        }
    }
    return users


# 2. Simulate Injective trades
def fetch_dummy_trades():
    trades = [
        {
            "direction": "buy",
            "price": 20.0,
            "quantity": 18.75,
            "timestamp": datetime(2024, 9, 3)
        },
        {
            "direction": "sell",
            "price": 25.0,
            "quantity": 10.0,
            "timestamp": datetime(2024, 9, 5)
        },
         {
            "direction": "buy",
            "price": 20.0,
            "quantity": 18.75,
            "timestamp": datetime(2024, 9, 3)
        }
    ]
    return trades


# 3. Process trades
def process_trades(users, trades):
    for trade in trades:
        trade_date = trade["timestamp"]
        price = trade["price"]

        if trade["direction"] == "buy":
            for user in users.values():
                if trade_date >= user["deposit_date"]:
                    invest_amount = user["remaining_cash"] * 0.25
                    if invest_amount > 0:
                        qty = invest_amount / price
                        user["remaining_cash"] -= invest_amount
                        user["token_balance"] += qty
                        user["actual_invested"] += invest_amount  # For display only

        elif trade["direction"] == "sell":
            total_tokens = sum(user["token_balance"] for user in users.values())
            if total_tokens == 0:
                continue
            for user in users.values():
                share = user["token_balance"] / total_tokens
                qty_to_sell = trade["quantity"] * share
                proceeds = qty_to_sell * price
                user["token_balance"] -= qty_to_sell
                user["remaining_cash"] += proceeds
                user["profit"] += proceeds  # optional tracking

    return users


# 4. Display result
def display_dashboard(users):
    for wallet, user in users.items():
        token_value = user["token_balance"] * CURRENT_PRICE
        current_value = user["remaining_cash"] + token_value
        profit = current_value - user["deposit"]
        roi = (profit / user["deposit"]) * 100 if user["deposit"] > 0 else 0

        print(f"\n📊 Wallet: {wallet}")
        print(f"Total Deposit: ${user['deposit']:.2f}")
        print(f"Actual Invested: ${user['actual_invested']:.2f}")
        print(f"Current Token Value: ${token_value:.2f}")
        print(f"Current Value: ${current_value:.2f}")
        print(f"Tokens: {user['token_balance']:.4f}")
        print(f"Cash: ${user['remaining_cash']:.2f}")
        print(f"Profit: {'+' if profit >= 0 else '-'}${abs(profit):.2f}")
        print(f"ROI: {'+' if roi >= 0 else '-'}{abs(roi):.2f}%")


# 5. Run
def main():
    users = fetch_dummy_users()
    trades = fetch_dummy_trades()
    updated_users = process_trades(users, trades)
    display_dashboard(updated_users)


if __name__ == "__main__":
    main()
