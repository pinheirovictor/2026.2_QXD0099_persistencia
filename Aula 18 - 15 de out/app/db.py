from typing import Any

from fastapi import Request
from pymongo import AsyncMongoClient, ASCENDING

from config import settings

async def setup_database(client: AsyncMongoClient) -> Any:
    db = client[settings.mongo_database]
    await db.command("ping")
    await db.produtos.create_index([("categoria", ASCENDING), ("ativo", ASCENDING)])
    await db.pedidos.create_index([("status", ASCENDING), ("criado_em", ASCENDING)])
    await db.pedido.create_index("cliente")
    return db

def get_db(request: Request):
    return request.app.state.db