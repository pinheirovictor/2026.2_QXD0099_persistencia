from typing import Union
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from http import HTTPStatus
import csv
import os

app = FastAPI()
CSV_FILE = "database.csv"

class Produto(BaseModel):
    id: int
    nome: str
    preco: float
    qtd: int
    
def ler_dados_csv():
    produtos = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r", newline="") as file:
            reader =  csv.DictReader(file)
            for row in reader:
                produtos.append(Produto(**row))
    return produtos

def escrever_dados_csv(produtos):
    with open(CSV_FILE, mode="w", newline="") as file:
        fieldnames = ["id", "nome", "preco", "qtd"]
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        for produto in produtos:
            writer.writerow(produto.dict())
            
@app.get("/produtos", response_model=List[Produto])
def listar_produtos():
    return ler_dados_csv()

@app.get("/produtos/{produto_id}", response_model=Produto)
def obter_produto(produto_id: int):
    produtos = listar_produtos()
    for produto in produtos:
        if produto.id == produto_id:
            return produto
    raise HTTPException(status_code=404, 
                        detail="Produto não encontrado")
    
@app.post("/produtos", response_model=Produto)
def criar_produto(produto: Produto):
    produtos = listar_produtos()
    if any(p.id == produto.id for p in produtos):
        raise HTTPException(status_code=400, detail="Id já existe")
    produtos.append(produto)
    escrever_dados_csv(produtos)
    return produto

@app.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, produto_atualizado: Produto):
    produtos = listar_produtos()
    for i, produto in enumerate(produtos):
        if produto.id == produto_id:
            produtos[i] = produto_atualizado
            escrever_dados_csv(produtos)
            return produto_atualizado
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.delete("/produtos/{produto_id}", response_model=dict)
def deletar_produto(produto_id: int):
    produtos = listar_produtos()
    produtos_filtrados = [produto for produto in produtos 
                          if produto.id != produto_id]
    if len(produtos) == len(produtos_filtrados):
        raise HTTPException(status_code=404, 
                            detail="Produto não encontrado")
    escrever_dados_csv(produtos_filtrados)
    return {"mensagem": "Produto deletado com sucesso"}
    