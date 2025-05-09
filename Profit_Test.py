from pymongo import MongoClient

def get_sample_trades():
    return [
        # Buys
        {
            "order_hash": "0xgeneratedhashbuy1",
            "direction": "buy",
            "price": 15.00,
            "quantity": 10.00,
            "fee": 0.00
        },
        {
            "order_hash": "0xgeneratedhashbuy2",
            "direction": "buy",
            "price": 12.00,
            "quantity": 12.00,
            "fee": 0.00
        },
        {
            "order_hash": "0xgeneratedhashbuy3",
            "direction": "buy",
            "price": 10.00,
            "quantity": 13.00,
            "fee": 0.00
        },
        # Sells
        {
            "order_hash": "0xgeneratedhashsell1",
            "direction": "sell",
            "price": 15.00,
            "quantity": 15.00,
            "fee": 0.00000003
        },
        {
            "order_hash": "0xgeneratedhashsell2",
            "direction": "sell",
            "price": 20.00,
            "quantity": 20.00,
            "fee": 0.00000003
        }
    ]


def calculate_overall_pnl(trades):
    total_bought_qty = 0.0
    total_bought_cost = 0.0
    total_sold_qty = 0.0
    total_sold_revenue = 0.0
    total_fees = 0.0

    for trade in trades:
        direction = trade["direction"]
        price = trade["price"]
        qty = trade["quantity"]
        fee = trade["fee"]

        if direction == "buy":
            total_bought_qty += qty
            total_bought_cost += price * qty
        elif direction == "sell":
            total_sold_qty += qty
            total_sold_revenue += price * qty
            total_fees += fee

    if total_bought_qty == 0:
        avg_buy_price = 0
    else:
        avg_buy_price = total_bought_cost / total_bought_qty

    cost_of_sold_tokens = avg_buy_price * total_sold_qty
    profit = total_sold_revenue - cost_of_sold_tokens - total_fees
    roi = (profit / cost_of_sold_tokens) * 100 if cost_of_sold_tokens > 0 else 0
    current_position = total_bought_qty - total_sold_qty

    return {
        "total_buy_qty": total_bought_qty,
        "avg_buy_price": avg_buy_price,
        "total_sell_qty": total_sold_qty,
        "avg_sell_price": total_sold_revenue / total_sold_qty if total_sold_qty else 0,
        "total_revenue": total_sold_revenue,
        "total_cost": total_bought_cost,
        "profit": profit,
        "roi": roi,
        "net_position": current_position
    }


def display_result():
    trades = get_sample_trades()
    stats = calculate_overall_pnl(trades)

    # Connect to the local MongoDB instance
    client = MongoClient("mongodb://localhost:27017/")
    db = client["vaultDB"]

    # Access a specific collection
    collection = db["transactions"]
    for doc in collection.find():
        print(doc)

    print("----- Position Summary -----")
    print(f"Total Bought: {stats['total_buy_qty']:.4f} tokens")
    print(f"Average Buy Price: {stats['avg_buy_price']:.4f} USD")
    print(f"Total Sold: {stats['total_sell_qty']:.4f} tokens")
    print(f"Average Sell Price: {stats['avg_sell_price']:.4f} USD")
    print(f"Total Revenue from Sells: {stats['total_revenue']:.4f} USD")
    print(f"Profit/Loss: {'+' if stats['profit'] >= 0 else '-'}{abs(stats['profit']):.4f} USD")
    print(f"ROI: {'+' if stats['roi'] >= 0 else '-'}{abs(stats['roi']):.2f}%")
    print(f"Current Net Position: {stats['net_position']:.4f} tokens")
    print("-----------------------------")


if __name__ == "__main__":
    display_result()
