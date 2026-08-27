from typing import Union
from typing import List
from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    nome: str
    valor: float
    is_oferta: Union[bool, None] = None

itens: List[Item] = []

@app.get("/")
def padrao():
    return {"msg": "Hello World"}

@app.get("/itens/{item_id}", response_model=Item)
def ler_item(item_id: int):
    for indice, item_atual in enumerate(itens):
        if item_atual.id == item_id:
            return item_atual
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item não encontrado.")

@app.get("/itens/", response_model=List[Item])
def listar_itens():
    return itens

@app.post("/itens/", response_model=Item, status_code=HTTPStatus.CREATED)
def adicionar_item(item: Item):
    if any(item_atual.id == item.id for item_atual in itens):
        raise HTTPException(status_code=400, detail="ID já existe.")
    itens.append(item)
    return item

@app.put("/itens/{item_id}", response_model=Item)
def atualizar_item(item_id: int, item_atualizado: Item):
    for indice, item_atual in enumerate(itens):
        if item_atual.id == item_id:
            if item_atualizado.id != item_id:
                item_atualizado.id = item_id
        itens[indice] = item_atualizado
        return item_atualizado
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item não encontrado.")


