import psycopg2
from fastapi import FastAPI, HTTPException, status

import crud

from models import (
    ClubeCreate,
    ClubeUpdate,
)

app = FastAPI(
    title="API de astronomia",
    description="FASTAPI + DB_API + POSTGRESQL, sem ORM",
    version="1.0.0"
)

def erro_404(recurso):
    raise HTTPException(
        status_code=404,
        detail=f"{recurso} não encontrado"
    )
    
@app.post("/clubes", status_code=201, tags=["Clubes"])
def criar_clube(dados: ClubeCreate):
    try:
        return crud.criar_clube(dados)
    except psycopg2.IntegrityError as erro:
        raise HTTPException(
            status_code=409,
            detail="Já existe um clube com esse ID",
        )from erro
        
@app.get("/clubes", tags=["Clubes"])
def listar_clubes():
    return crud.listar_clubes()

