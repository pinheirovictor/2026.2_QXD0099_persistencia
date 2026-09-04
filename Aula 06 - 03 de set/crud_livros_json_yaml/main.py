from fastapi import FastAPI

from routes.livros import router as livros_router
from core.logging_config import logger


app = FastAPI(
    title="QXD0099 - API de Livros",
    description=(
        "API didática com FastAPI, persistência em JSON "
        "e logging configurado por YAML."
    ),
    version="1.0.0",
)

app.include_router(livros_router)


@app.get("/", tags=["Sistema"])
def home():
    logger.info("Endpoint raiz acessado.")

    return {
        "mensagem": "API de Livros - Persistência em JSON",
        "recursos": [
            "/livros",
            "/docs",
            "/redoc",
        ],
    }
