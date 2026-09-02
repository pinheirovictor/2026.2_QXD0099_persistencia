from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import json
import csv
import os

app = FastAPI()

ARQUIVO_JSON = "alunos.json"
ARQUIVO_CSV = "alunos.csv"

class Aluno(BaseModel):
    nome: str
    idade: int
    curso: str
    
def carregar_alunos():
    if not os.path.exists(ARQUIVO_JSON):
        return []
    with open(ARQUIVO_JSON, 'r', encoding="utf-8") as arquivo:
        return json.load(arquivo)

def salvar_alunos(alunos):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(
            alunos, 
            arquivo,
            indent=4,
            ensure_ascii=False
        )

@app.get("/alunos")
def listar_alunos():
    return carregar_alunos()

@app.post("/alunos")
def cadastrar_aluno(aluno: Aluno):
    alunos = carregar_alunos()
    
    novo_aluno = aluno.dict()
    
    novo_aluno["id"] = len(alunos) + 1
    
    alunos.append(novo_aluno)
    
    salvar_alunos(alunos)
    
    return novo_aluno


@app.get("/alunos/exportar/csv")
def exportar_csv():
    alunos = carregar_alunos()
    
    if not alunos:
        raise HTTPException(
            status_code=404, 
            detail="Nenhum aluno cadastrado"
        )
    
    with open(
        ARQUIVO_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        campos = ["id", "nome", "idade", "curso"]
        
        writer = csv.DictWriter(
            arquivo, 
            fieldnames=campos
        )
        
        writer.writeheader()
        writer.writerows(alunos)
        
        return{
            "mensagem": "Arquivo CSV exportado com sucesso",
            "arquivo": ARQUIVO_CSV
        }