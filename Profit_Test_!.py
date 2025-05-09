from datetime import datetime

# Constants
CURRENT_PRICE = 22.0

# 1. Simulate user transactions
def fetch_dummy_users():
    users = {
        "wallet_1": {
            "deposit": 1000.0,
            "deposit_date": datetime(2024, 9, 1),
            "remaining_cash": 1000.0,
            "token_balance": 0.0,
            "profit": 0.0,
            "actual_invested": 0.0
        },
        "wallet_2": {
            "deposit": 1000.0,
            "deposit_date": datetime(2024, 9, 3),
            "remaining_cash": 1000.0,
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
            "quantity": 20.0,
            "timestamp": datetime(2024, 9, 2),  # Only wallet_1 exists
        },
        {
            "direction": "buy",
            "price": 25.0,
            "quantity": 16.0,
            "timestamp": datetime(2024, 9, 4),  # Both wallets active
        },
        {
            "direction": "sell",
            "price": 23.0,
            "quantity": 20.0,
            "timestamp": datetime(2024, 9, 5),  # Sell some of the tokens
        }
    ]
    return trades


# 3. Process trades (no fixed %)
def process_trades(users, trades):
    for trade in trades:
        trade_date = trade["timestamp"]
        price = trade["price"]
        quantity = trade["quantity"]

        if trade["direction"] == "buy":
            # Filter only eligible users based on deposit date
            eligible_users = {w: u for w, u in users.items() if trade_date >= u["deposit_date"]}
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
                user_tokens_to_sell = trade["quantity"] * user_share
                user_proceeds = user_tokens_to_sell * price

                user["token_balance"] -= user_tokens_to_sell
                user["remaining_cash"] += user_proceeds
                user["profit"] += user_proceeds

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


# 5. Run it
def main():
    users = fetch_dummy_users()
    trades = fetch_dummy_trades()
    updated_users = process_trades(users, trades)
    display_dashboard(updated_users)


if __name__ == "__main__":
    main()
