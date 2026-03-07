import time
import requests
import pandas as pd
from src.config import TWELVEDATA_API_KEY

BASE_URL = "https://api.twelvedata.com/time_series"

def fetch_time_series(symbol: str, interval: str = "1day", outputsize: int = 5000) -> pd.DataFrame:
    if not TWELVEDATA_API_KEY:
        raise RuntimeError("Missing TWELVEDATA_API_KEY in environment/.env")

    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": TWELVEDATA_API_KEY,
        "format": "JSON",
    }

    r = requests.get(BASE_URL, params=params, timeout=30)
    r.raise_for_status()
    payload = r.json()

    if "status" in payload and payload["status"] == "error":
        raise RuntimeError(f"TwelveData error for {symbol}: {payload}")

    values = payload.get("values", [])
    if not values:
        return pd.DataFrame(columns=["datetime", "open", "high", "low", "close", "volume"])

    df = pd.DataFrame(values)
    df["symbol"] = symbol
    df["timeframe"] = interval
    return df

def fetch_many(symbols, interval="1day", outputsize=5000, sleep_s=8.0) -> pd.DataFrame:
    frames = []
    for i, sym in enumerate(symbols, start=1):
        df = fetch_time_series(sym, interval=interval, outputsize=outputsize)
        frames.append(df)
        if i < len(symbols):
            time.sleep(sleep_s)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()