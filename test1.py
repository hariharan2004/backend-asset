from Signal.matest import ma_signals
import asyncio

async def main():
    data_path = "/home/hariharan/Crypt/BTC_DAILY/Bitcoin_Historical_Data_Daily.csv"

    ma_signal_df = await ma_signals(data_path)
    
    if not ma_signal_df.empty:
        print("Moving Average Signal:", ma_signal_df["Moving Average"].iloc[0])
    else:
        print("Moving Average Signal DataFrame is empty.")

if __name__ == "__main__":
    asyncio.run(main())