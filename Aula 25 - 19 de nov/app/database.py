from functools import lru_cache
from pymongo import ASCENDING, MongoClient
from pymongo.database import Database

from app.config import mongo_db_name, mongo_uri

@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    return MongoClient(mongo_uri(), serverSelectionTimeoutMS=4000)

def get_db() -> Database:
    return get_client()[mongo_db_name()]

def criar_indices(db: Database) -> None:
    # Índices de consulta e das chaves utilizadas nos relacionamentos.
    for collection, indexes in {
        "candidatos": [
            [("municipio", ASCENDING), ("cargo", ASCENDING)],
            [("uf", ASCENDING), ("partido", ASCENDING)],
            [("chave_candidato", ASCENDING)],
            [("chave_coligacao", ASCENDING)],
            [("chave_vaga", ASCENDING)],
            [("data_eleicao", ASCENDING)],
        ],
        "bens": [
            [("chave_candidato", ASCENDING)],
            [("municipio", ASCENDING)],
            [("tipo_bem", ASCENDING)],
            [("data_atualizacao", ASCENDING)],
        ],
        "coligacoes": [
            [("chave_coligacao", ASCENDING)],
            [("municipio", ASCENDING), ("cargo", ASCENDING)],
            [("partido", ASCENDING)],
        ],
        "vagas": [
            [("chave_vaga", ASCENDING)],
            [("municipio", ASCENDING), ("cargo", ASCENDING)],
        ],
        "redes_sociais": [
            [("chave_candidato", ASCENDING)],
            [("dominio", ASCENDING)],
        ],
    }.items():
        for index in indexes:
            db[collection].create_index(index)

