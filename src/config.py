import os
from dotenv import load_dotenv

load_dotenv()

TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY", "")

DB = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "name": os.getenv("DB_NAME", "aurumfx"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

SYMBOLS = ["XAU/USD", "EUR/USD", "GBP/USD", "USD/ZAR"]
TIMEFRAME = "1day"
OUTPUTSIZE = 5000
SOURCE = "twelvedata"