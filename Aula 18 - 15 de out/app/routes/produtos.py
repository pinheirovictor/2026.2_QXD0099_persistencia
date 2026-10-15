from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pymongo import ASCENDING, ReturnDocument

from db import get_db
from models import ProdutoEntrada, ProdutoAtualizacao, ProdudoSaida, Mensagem

from utils import object_id, to_api

router = APIRouter(
    prefix="/produtos", 
    tags=["Produtos"]
    )

@router.post("", response_model=ProdudoSaida, status_code=201)
async def criar_produto(data: ProdutoEntrada, db = Depends(get_db)):
    doc = data.model_dump()
    result = await db.produtos.insert_one(doc)
    doc["_id"] = result.inserted_id
    return to_api(doc)
    
@router.get("/{produto_id}", response_model=ProdudoSaida)
async def buscar_produto(produto_id: int, db = Depends(get_db)):
    doc = await db.produtos.find_one({"_id": object_id(produto_id)})
    if doc is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return to_api(doc)


@router.patch("/{produto_id}", response_model=ProdudoSaida)
async def atualizar_produto(produto_id: int, data: ProdutoAtualizacao, db = Depends(get_db)):
    alteracoes = data.model_dump(exclude_unset=True)
    
    if not alteracoes:
        raise HTTPException(status_code=422, detail="Informe pelo menos 1 campo pra atualizar")
    doc = await db.produtos.find_one_and_update(
        {"_id": object_id(produto_id)}, 
        {"$set": alteracoes},
        return_document=ReturnDocument.AFTER
    )
    
    if doc is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return to_api(doc)