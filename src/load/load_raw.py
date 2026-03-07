import pandas as pd
from sqlalchemy import text
from src.load.db import get_engine
from src.extract.fetch_prices import fetch_many
from src.config import SYMBOLS, TIMEFRAME, OUTPUTSIZE, SOURCE

def upsert_raw(df: pd.DataFrame) -> int:
    if df.empty:
        return 0

    df = df.copy()
    df.rename(columns={"datetime": "ts"}, inplace=True)

    keep = ["symbol", "timeframe", "ts", "open", "high", "low", "close", "volume"]
    for col in keep:
        if col not in df.columns:
            df[col] = None
    df = df[keep]
    df["source"] = SOURCE

    engine = get_engine()

    with engine.begin() as conn:
        df.to_sql("raw_candles_tmp", conn, if_exists="replace", index=False)

        sql = """
        INSERT INTO raw_candles (symbol, timeframe, ts, open, high, low, close, volume, source)
        SELECT symbol, timeframe, ts::timestamptz, open::numeric, high::numeric, low::numeric, close::numeric, volume::numeric, source
        FROM raw_candles_tmp
        ON CONFLICT (symbol, timeframe, ts) DO NOTHING;
        """
        conn.execute(text(sql))
        conn.execute(text("DROP TABLE IF EXISTS raw_candles_tmp;"))

    return len(df)

def main():
    df = fetch_many(SYMBOLS, interval=TIMEFRAME, outputsize=OUTPUTSIZE)
    n = upsert_raw(df)
    print(f"Loaded ~{n} raw rows for {len(SYMBOLS)} symbols.")

if __name__ == "__main__":
    main()