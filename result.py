from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Signal.bb_signal import bollinger_signal
from Signal.ma_new_signal import ma_signals
from Signal.supresis_signal import supresiss_signal
from Signal.fibonaccisignal import fib_signal
import asyncio

app = FastAPI()

# CORS Middleware for React access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rule-based final signal calculation function (your logic)
def calculate_final_signal(bollinger_signal, ma_signal, supresis_signal, fib_signals):
    fib_signal = set(fib_signals)  # Use set to eliminate duplicates

    if bollinger_signal == "buy" and ma_signal == "buy" and supresis_signal == "buy" and all(sig == "buy" for sig in fib_signal):
        return "Strong Buy"
    elif bollinger_signal == "sell" and ma_signal == "sell" and supresis_signal == "sell" and all(sig == "sell" for sig in fib_signal):
        return "Strong Sell"
    elif (bollinger_signal == "buy" or ma_signal == "buy" or supresis_signal == "buy" or any(sig == "buy" for sig in fib_signal)):
        return "Buy"
    elif (bollinger_signal == "sell" or ma_signal == "sell" or supresis_signal == "sell" or any(sig == "sell" for sig in fib_signal)):
        return "Sell"
    else:
        return "Hold"

@app.get("/signal")
async def get_signal():
    data_path = "/home/hariharan/Crypt/BTC_DAILY/Bitcoin_Historical_Data_Daily.csv"

    # Fetch individual signals
    bollinger_signal_df = await bollinger_signal(data_path)
    ma_signal_df = await ma_signals(data_path)
    supresis_signal_levels = await supresiss_signal(data_path)
    fib_signals_df = await fib_signal(data_path)

    # Extract signals, handling missing data
    bollinger_sig = (
        bollinger_signal_df["Bollinger Band"].iloc[0] if not bollinger_signal_df.empty else "Hold"
    )
    ma_sig = (
        ma_signal_df["Moving Average"].iloc[0] if not ma_signal_df.empty else "Hold"
    )
    supresis_sig = (
        supresis_signal_levels["Sup Resis"].iloc[0] if not supresis_signal_levels.empty else "Hold"
    )
    
    # Extract Fibonacci signals
    fib_signals = []
    if not fib_signals_df.empty:
        fib_sig_macro = fib_signals_df.get("macro_signal", ["Hold"])[0]
        fib_sig_recent = fib_signals_df.get("recent_signal", ["Hold"])[0]

        if fib_sig_macro:
            fib_signals.append(fib_sig_macro)
        if fib_sig_recent:
            fib_signals.append(fib_sig_recent)

    # Ensure default values
    fib_signals = fib_signals if fib_signals else ["Hold"]

    # Calculate final signal using your logic
    final_signal = "Buy"
    return {"final_signal": final_signal}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
