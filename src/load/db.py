from sqlalchemy import create_engine
from src.config import DB

def get_engine():
    url = (
        f"postgresql+psycopg2://{DB['user']}:{DB['password']}"
        f"@{DB['host']}:{DB['port']}/{DB['name']}"
    )
    return create_engine(url, pool_pre_ping=True)