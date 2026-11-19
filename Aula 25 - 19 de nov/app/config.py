
import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

@lru_cache
def mongo_uri() -> str:
    return os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")

@lru_cache
def mongo_db_name() -> str:
    return os.getenv("MONGO_DB", "eleicoes_2024")