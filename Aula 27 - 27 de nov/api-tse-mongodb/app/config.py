"""Configurações obtidas de variáveis de ambiente (ou do arquivo .env)."""

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@lru_cache
def mongo_uri() -> str:
    return os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017")


@lru_cache
def mongo_db_name() -> str:
    return os.getenv("MONGODB_DB", "eleicoes_2024")
